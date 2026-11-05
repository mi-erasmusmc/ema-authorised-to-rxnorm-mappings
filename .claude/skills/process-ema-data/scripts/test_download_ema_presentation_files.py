"""Offline regression tests for interrupted and incremental EMA downloads."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import pandas as pd
import requests

import download_ema_presentation_files as downloader
import fetch_ema_updates as updater


PDF = b'%PDF-1.7\nfixture\n%%EOF\n'
PRODUCT = 'EMEA/H/C/000001'
FILENAME = '000001_example_2026-01-02.pdf'

def document(product=PRODUCT, date='2026-01-02T01:00:00Z', **changes):
    result = dict(type='all-authorised-presentations', ema_product_number=product,
                  document_url='https://www.ema.europa.eu/en/documents/all-authorised-presentations/example_en.pdf',
                  first_published_date='2025-01-01T01:00:00Z', last_updated_date=date)
    result.update(changes)
    return result


def feed(records):
    return dict(meta=dict(total_records=len(records)), data=records)


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.folder = self.root / 'products' / '000001'
        self.folder.mkdir(parents=True)
        self.pdf = self.folder / FILENAME
        self.progress = self.root / downloader.PROGRESS_FILE
        self.df = pd.DataFrame([{
            'EMA product number': PRODUCT, 'Name of medicine': 'Example',
            'Medicine URL': 'https://example.com/medicine', 'Category': 'Human',
            'First published date': '01/01/2026', 'Last updated date': '03/01/2026',
        }])
        self.documents = [document()]
        self.record = dict(
            ema_product_number=PRODUCT, medicine_name='Example',
            medicine_url='https://example.com/medicine', pdf_url='https://example.com/a.pdf',
            last_updated='02/01/2026', pdf_filename=FILENAME, status='success',
            report_dates='01/01/2026|03/01/2026',
        )
        self.session = Mock()
        self.session.get.return_value.status_code = 200
        self.session.get.return_value.content = PDF
        self.enterContext(patch.object(downloader.time, 'sleep'))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))
        self.enterContext(contextlib.redirect_stderr(io.StringIO()))

    def process(self, **kwargs):
        index = downloader.build_presentation_index(feed(self.documents)) if self.documents else {}
        return downloader.process_medicines(self.df, str(self.root), self.session,
                                           presentation_index=index, **kwargs)

    def save_record(self, **changes):
        self.record.update(changes)
        downloader.save_progress(self.progress, [self.record])

    def test_current_pdf_requires_no_network_even_without_progress(self):
        self.pdf.write_bytes(PDF)
        result = self.process()
        self.session.get.assert_not_called()
        self.assertEqual(result['pending'], 0)
        self.assertEqual(downloader.load_progress(self.progress)[PRODUCT]['status'], 'success')

    def test_missing_pdf_recovers_despite_success_record(self):
        self.save_record()
        self.process()
        self.assertEqual(self.pdf.read_bytes(), PDF)
        self.session.get.assert_called_once_with(self.documents[0]['document_url'], timeout=60)

    def test_truncated_pdf_is_replaced(self):
        self.pdf.write_bytes(b'%PDF-1.7\nunfinished')
        self.save_record()
        self.process()
        self.assertEqual(self.pdf.read_bytes(), PDF)

    def test_medicine_report_dates_do_not_cause_network_requests(self):
        self.pdf.write_bytes(PDF)
        self.df.loc[0, 'Last updated date'] = '05/11/2026'
        self.process()
        self.session.get.assert_not_called()

    def test_new_document_is_downloaded_even_if_medicine_report_is_unchanged(self):
        self.pdf.write_bytes(PDF)
        self.documents[0]['last_updated_date'] = '2026-01-04T01:00:00Z'
        self.process()
        self.assertTrue((self.folder / '000001_example_2026-01-04.pdf').exists())
        self.session.get.assert_called_once()

    def test_saved_timestamp_detects_second_revision_on_same_day(self):
        self.pdf.write_bytes(PDF)
        self.process()
        self.documents[0]['last_updated_date'] = '2026-01-02T14:00:00Z'
        self.process()
        self.session.get.assert_called_once()

    def test_interrupted_same_day_revision_stays_pending_on_restart(self):
        self.pdf.write_bytes(PDF)
        self.process()
        self.documents[0]['last_updated_date'] = '2026-01-02T14:00:00Z'
        self.session.get.side_effect = KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            self.process()
        self.session.get.side_effect = None
        self.session.get.reset_mock()
        self.process()
        self.session.get.assert_called_once()
        self.process()
        self.session.get.assert_called_once()

    def test_saved_failures_never_prevent_missing_pdf_downloads(self):
        for status in ('download_failed', 'skipped_before_date', 'no_pdf_found'):
            with self.subTest(status=status):
                self.save_record(status=status, pdf_filename='')
                if self.pdf.exists():
                    self.pdf.unlink()
                self.process()
                self.assertEqual(self.pdf.read_bytes(), PDF)

    def test_unrelated_newest_pdf_does_not_hide_missing_product(self):
        (self.root / 'products' / 'unrelated').mkdir()
        (self.root / 'products' / 'unrelated' / 'other_2026-11-03.pdf').write_bytes(PDF)
        self.process()
        self.assertEqual(self.pdf.read_bytes(), PDF)

    def test_renamed_medicine_reuses_same_document(self):
        self.pdf.write_bytes(PDF)
        self.df.loc[0, 'Name of medicine'] = 'Renamed Example'
        self.process()
        self.session.get.assert_not_called()

    def test_newer_local_pdf_is_kept_when_feed_lags(self):
        (self.folder / '000001_example_2026-01-05.pdf').write_bytes(PDF)
        self.process()
        self.session.get.assert_not_called()

    def test_absent_document_needs_no_page_request(self):
        self.documents = []
        self.process()
        self.session.get.assert_not_called()
        self.assertEqual(downloader.load_progress(self.progress)[PRODUCT]['status'], 'no_pdf_in_index')


    def test_queue_is_persisted_before_rate_limit(self):
        self.session.get.return_value.status_code = 429
        with self.assertRaises(downloader.EMARateLimitError):
            self.process()
        self.assertEqual(downloader.load_progress(self.progress)[PRODUCT]['status'], 'pending')
        self.session.get.assert_called_once()

    def test_failed_pdf_remains_pending(self):
        self.session.get.side_effect = requests.ConnectionError('offline')
        result = self.process()
        self.assertEqual((result['failed'], result['pending']), (1, 1))
        self.assertEqual(downloader.load_progress(self.progress)[PRODUCT]['status'], 'download_failed')

    def test_dry_run_does_not_write_progress_or_download(self):
        result = self.process(dry_run=True)
        self.assertEqual(result['pending'], 1)
        self.assertFalse(self.progress.exists())
        self.session.get.assert_not_called()

    def test_since_filters_document_date_not_page_date(self):
        self.df.loc[0, 'Last updated date'] = '05/11/2026'
        result = self.process(since_date=downloader.parse_date('2026-01-03'))
        self.assertEqual(result['pending'], 0)
        self.session.get.assert_not_called()

    def test_index_selects_latest_document_for_duplicate_product(self):
        records = [document(), document(date='2026-01-04T01:00:00Z')]
        for ordered in (records, list(reversed(records))):
            self.assertEqual(downloader.build_presentation_index(feed(ordered))[PRODUCT]['date'], '2026-01-04')

    def test_index_uses_publication_date_when_update_date_missing(self):
        record = document(last_updated_date='', first_published_date='2026-02-03T01:00:00Z')
        self.assertEqual(downloader.build_presentation_index(feed([record]))[PRODUCT]['date'], '2026-02-03')

    def test_index_preserves_official_pdf_dash_zero_urls(self):
        record = document(document_url='https://www.ema.europa.eu/en/documents/example_en.pdf-0')
        self.assertEqual(downloader.build_presentation_index(feed([record]))[PRODUCT]['document_url'],
                         record['document_url'])

    def test_document_dates_use_amsterdam_calendar_date(self):
        record = document(date='2026-01-01T23:30:00Z')
        self.assertEqual(downloader.build_presentation_index(feed([record]))[PRODUCT]['date'], '2026-01-02')

    def test_incomplete_or_invalid_feed_fails_instead_of_claiming_no_pdfs(self):
        for invalid in ({}, {'data': []}, feed([]), dict(meta=dict(total_records=2), data=[document()])):
            with self.subTest(payload=invalid), self.assertRaises(ValueError):
                downloader.build_presentation_index(invalid)

    def test_index_ignores_other_document_types_and_veterinary_products(self):
        records = [document(), document(type='assessment-report'), document('EMEA/V/C/000002')]
        self.assertEqual(list(downloader.build_presentation_index(feed(records))), [PRODUCT])

    def test_pdf_and_index_rate_limits_are_not_retried(self):
        self.session.get.return_value.status_code = 429
        for action in (
            lambda: downloader.download_presentation_index(self.session),
            lambda: downloader.download_pdf('https://example.com/a.pdf', self.pdf, self.session),
        ):
            self.session.get.reset_mock()
            with self.assertRaises(downloader.EMARateLimitError):
                action()
            self.session.get.assert_called_once()

    def test_rate_limit_diagnostic_includes_retry_after_and_url(self):
        response = requests.Response()
        response.status_code = 429
        response.url = 'https://example.com/page'
        response.headers['Retry-After'] = '300'
        message = str(downloader.EMARateLimitError.from_response(response))
        self.assertIn('Retry-After: 300', message)
        self.assertIn(response.url, message)
        response.headers.clear()
        self.assertIn('No Retry-After header supplied',
                      str(downloader.EMARateLimitError.from_response(response)))

    def test_session_does_not_automatically_retry_429(self):
        session = downloader.get_session_with_retries()
        self.addCleanup(session.close)
        retry = session.get_adapter('https://').max_retries
        self.assertFalse(retry.is_retry('GET', 429, has_retry_after=True))
        self.assertEqual(retry.total, 0)

    def test_decimal_retry_after_waits_then_retries_same_request(self):
        adapter = downloader.PacedHTTPAdapter(1)
        self.addCleanup(adapter.close)
        limited = Mock(status_code=429, headers={'Retry-After': '10.000'})
        success = Mock(status_code=200)
        request = requests.Request('GET', 'https://example.com/a.pdf').prepare()
        with patch.object(downloader.HTTPAdapter, 'send', side_effect=[limited, success]) as send, \
                patch.object(downloader.time, 'monotonic', return_value=0), \
                patch.object(downloader.time, 'sleep') as sleep:
            self.assertIs(adapter.send(request), success)
        sleep.assert_called_once_with(10)
        self.assertEqual(send.call_count, 2)
        self.assertTrue(all(call.args[0] is request for call in send.call_args_list))
        limited.close.assert_called_once()

    def test_persistent_rate_limit_has_bounded_retries(self):
        adapter = downloader.PacedHTTPAdapter(1)
        self.addCleanup(adapter.close)
        limited = Mock(status_code=429, headers={'Retry-After': '10.000'})
        request = requests.Request('GET', 'https://example.com/a.pdf').prepare()
        with patch.object(downloader.HTTPAdapter, 'send', return_value=limited) as send, \
                patch.object(downloader.time, 'monotonic', return_value=0), \
                patch.object(downloader.time, 'sleep') as sleep:
            self.assertIs(adapter.send(request), limited)
        self.assertEqual(send.call_count, 4)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [10, 10, 10])

    def test_missing_invalid_or_long_retry_after_stops_without_retry(self):
        for header in (None, '', 'invalid', '-1', 'nan', 'inf', '301'):
            with self.subTest(header=header):
                adapter = downloader.PacedHTTPAdapter(1)
                self.addCleanup(adapter.close)
                limited = Mock(status_code=429, headers={'Retry-After': header})
                request = requests.Request('GET', 'https://example.com').prepare()
                with patch.object(downloader.HTTPAdapter, 'send', return_value=limited) as send, \
                        patch.object(downloader.time, 'monotonic', return_value=0), \
                        patch.object(downloader.time, 'sleep') as sleep:
                    self.assertIs(adapter.send(request), limited)
                send.assert_called_once()
                sleep.assert_not_called()

    def test_retry_after_accepts_http_dates_and_decimal_seconds(self):
        self.assertEqual(downloader.parse_retry_after('10.000'), 10)
        self.assertEqual(downloader.parse_retry_after('0.5'), 0.5)
        with patch.object(downloader.time, 'time', return_value=990):
            self.assertEqual(downloader.parse_retry_after('Thu, 01 Jan 1970 00:16:40 GMT'), 10)

    def test_retry_after_never_shortens_configured_spacing(self):
        adapter = downloader.PacedHTTPAdapter(30)
        self.addCleanup(adapter.close)
        limited = Mock(status_code=429, headers={'Retry-After': '10.000'})
        success = Mock(status_code=200)
        request = requests.Request('GET', 'https://example.com').prepare()
        with patch.object(downloader.HTTPAdapter, 'send', side_effect=[limited, success]), \
                patch.object(downloader.time, 'monotonic', return_value=0), \
                patch.object(downloader.time, 'sleep') as sleep:
            self.assertIs(adapter.send(request), success)
        sleep.assert_called_once_with(30)

    def test_every_request_is_paced_and_elapsed_time_counts(self):
        adapter = downloader.PacedHTTPAdapter(30)
        self.addCleanup(adapter.close)
        with patch.object(downloader.HTTPAdapter, 'send') as send, \
                patch.object(downloader.time, 'monotonic', side_effect=[10, 15, 40, 80, 90]), \
                patch.object(downloader.time, 'sleep') as sleep:
            for url in ('https://example.com/report.xlsx', 'https://example.com/page',
                        'https://example.com/presentation.pdf'):
                adapter.send(requests.Request('GET', url).prepare())
        self.assertEqual(send.call_count, 3)
        sleep.assert_called_once_with(25)

    def test_failed_request_also_starts_the_wait_interval(self):
        adapter = downloader.PacedHTTPAdapter(30)
        self.addCleanup(adapter.close)
        with patch.object(downloader.HTTPAdapter, 'send', side_effect=[requests.ConnectionError(), Mock()]), \
                patch.object(downloader.time, 'monotonic', side_effect=[10, 15, 40]), \
                patch.object(downloader.time, 'sleep') as sleep:
            with self.assertRaises(requests.ConnectionError):
                adapter.send(Mock())
            adapter.send(Mock())
        sleep.assert_called_once_with(25)

    def test_custom_interval_is_shared_between_http_and_https(self):
        session = downloader.get_session_with_retries(request_interval=60)
        self.addCleanup(session.close)
        self.assertIs(session.get_adapter('http://'), session.get_adapter('https://'))
        self.assertEqual(session.get_adapter('https://').request_interval, 60)

    def test_invalid_intervals_are_rejected(self):
        for value in ('0', '-1', 'nan', 'inf'):
            with self.subTest(value=value), self.assertRaises(downloader.argparse.ArgumentTypeError):
                downloader.positive_seconds(value)

    def test_progress_replacement_is_atomic(self):
        self.save_record()
        before = self.progress.read_bytes()
        with patch.object(downloader.os, 'replace', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.save_record(status='download_failed')
        self.assertEqual(self.progress.read_bytes(), before)

    def test_bad_response_does_not_overwrite_existing_pdf(self):
        self.pdf.write_bytes(PDF)
        self.session.get.return_value.content = b'<html>Error</html>'
        self.assertFalse(downloader.download_pdf('https://example.com/a.pdf', self.pdf, self.session))
        self.assertEqual(self.pdf.read_bytes(), PDF)

    def test_interrupted_write_does_not_publish_final_pdf(self):
        with patch.object(downloader.os, 'replace', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                downloader.download_pdf('https://example.com/a.pdf', self.pdf, self.session)
        self.assertFalse(self.pdf.exists())

    def test_wrapper_has_no_automatic_global_cutoff(self):
        with patch.object(updater.sys, 'argv', ['fetch_ema_updates.py']), \
                patch.object(updater, 'download_excel_file', return_value='report.xlsx'), \
                patch.object(updater, 'convert_excel_to_tsv', return_value=('report.tsv', self.df)), \
                patch.object(updater, 'get_session_with_retries'), \
                patch.object(updater, 'generate_ema_info_main'), \
                patch.object(updater, 'regenerate_ema'), \
                patch.object(updater, 'process_medicines', return_value={'pending': 0, 'failed': 0}) as process:
            updater.main()
        self.assertIsNone(process.call_args.kwargs['since_date'])


if __name__ == '__main__':
    unittest.main()

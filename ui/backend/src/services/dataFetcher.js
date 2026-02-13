import https from 'https';

const GITHUB_BASE_URL = 'https://raw.githubusercontent.com/mi-erasmusmc/ema-authorised-to-rxnorm-mappings/main';

const DATA_SOURCES = {
  mappings: `${GITHUB_BASE_URL}/ema-to-rxnorm.tsv`,
  productDetails: `${GITHUB_BASE_URL}/data/ema/combined_ema_products.tsv`,
  medicinesReport: `${GITHUB_BASE_URL}/data/ema/medicines_report.tsv`
};

/**
 * Fetch data from a URL
 * @param {string} url - URL to fetch
 * @returns {Promise<string>} - Response data
 */
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      if (response.statusCode === 302 || response.statusCode === 301) {
        // Follow redirect
        return fetchUrl(response.headers.location).then(resolve).catch(reject);
      }

      if (response.statusCode !== 200) {
        reject(new Error(`Failed to fetch ${url}: ${response.statusCode}`));
        return;
      }

      let data = '';
      response.on('data', (chunk) => {
        data += chunk;
      });

      response.on('end', () => {
        resolve(data);
      });
    }).on('error', (error) => {
      reject(error);
    });
  });
}

/**
 * Fetch EMA to RxNorm mappings
 * @returns {Promise<string>} TSV content
 */
export async function fetchMappings() {
  console.log('Fetching EMA to RxNorm mappings...');
  return fetchUrl(DATA_SOURCES.mappings);
}

/**
 * Fetch parsed PDF product details
 * @returns {Promise<string>} TSV content
 */
export async function fetchProductDetails() {
  console.log('Fetching product details...');
  return fetchUrl(DATA_SOURCES.productDetails);
}

/**
 * Fetch medicines report
 * @returns {Promise<string>} TSV content
 */
export async function fetchMedicinesReport() {
  console.log('Fetching medicines report...');
  return fetchUrl(DATA_SOURCES.medicinesReport);
}

/**
 * Fetch all required data sources
 * @returns {Promise<{mappings: string, productDetails: string, medicinesReport: string}>}
 */
export async function fetchAllData() {
  console.log('Starting data fetch from GitHub...');

  const [mappings, productDetails, medicinesReport] = await Promise.all([
    fetchMappings(),
    fetchProductDetails(),
    fetchMedicinesReport()
  ]);

  console.log('All data fetched successfully');

  return {
    mappings,
    productDetails,
    medicinesReport
  };
}

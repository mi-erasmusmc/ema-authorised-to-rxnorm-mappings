#!/usr/bin/env python3
"""
Download AEMPS prescription nomenclator and convert to TSV with decoded values.

Source: http://listadomedicamentos.aemps.gob.es/prescripcion.zip

List fields:
  - principios_activos: pipe-separated "NAME DOSE UNIT" per active ingredient
    (ordered by orden_colacion), e.g. "AMOXICILINA 500 mg|ACIDO CLAVULANICO 50 mg"
  - vias_administracion: pipe-separated route names, e.g. "INTRAVENOSA|ORAL"

Omitted fields:
  - duplicidades (ATC duplication alerts — reference metadata, not product data)
  - problemassuministro (supply problem notes)
"""

import csv
import io
import re
import ssl
import sys
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

URL = "http://listadomedicamentos.aemps.gob.es/prescripcion.zip"
OUT_TSV = Path(__file__).parent / "prescripcion.tsv"

COLUMNS = [
    "cod_nacion",
    "nro_definitivo",
    "des_nomco",
    "des_prese",
    "des_dcsa",
    "des_dcp",
    "des_dcpf",
    "des_dosific",
    "envase",
    "contenido",
    "unidad_contenido",
    "nro_conte",
    "sw_psicotropo",
    "sw_estupefaciente",
    "sw_afecta_conduccion",
    "sw_triangulo_negro",
    "url_fictec",
    "url_prosp",
    "sw_receta",
    "sw_generico",
    "sw_sustituible",
    "sw_envase_clinico",
    "sw_uso_hospitalario",
    "sw_diagnostico_hospitalario",
    "sw_tld",
    "sw_especial_control_medico",
    "sw_huerfano",
    "sw_base_a_plantas",
    "laboratorio_titular",
    "laboratorio_comercializador",
    "fecha_autorizacion",
    "sw_comercializado",
    "fec_comer",
    "situacion_registro",
    "situacion_registro_presen",
    "fecha_situacion_registro",
    "fec_sitreg_presen",
    "sw_tiene_excipientes_decl_obligatoria",
    "biosimilar",
    "importacion_paralela",
    "radiofarmaco",
    "serializacion",
    "forma_farmaceutica",
    "forma_farmaceutica_simplificada",
    "nro_pactiv",
    "principios_activos",
    "vias_administracion",
    "cod_atc",
    "des_atc",
]


def strip_namespaces(xml_bytes: bytes) -> bytes:
    """Remove all XML namespace declarations and prefixes for simpler parsing."""
    # Remove xmlns declarations
    xml_bytes = re.sub(rb' xmlns(?::[a-zA-Z0-9_]+)?="[^"]*"', b"", xml_bytes)
    # Remove namespace-prefixed attributes (e.g. xsi:schemaLocation="...")
    xml_bytes = re.sub(rb' [a-zA-Z0-9_]+:[a-zA-Z0-9_]+=(?:"[^"]*"|\'[^\']*\')', b"", xml_bytes)
    # Remove namespace prefixes from element tags
    xml_bytes = re.sub(rb"<([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)", rb"<\2", xml_bytes)
    xml_bytes = re.sub(rb"</([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)", rb"</\2", xml_bytes)
    return xml_bytes


def parse_dict(zf: zipfile.ZipFile, filename: str, key_tag: str, val_tag: str) -> dict:
    """Parse a dictionary XML file into a {key: value} mapping."""
    with zf.open(filename) as f:
        raw = strip_namespaces(f.read())
    root = ET.fromstring(raw)
    result = {}
    for elem in root:
        key = val = None
        for child in elem:
            if child.tag == key_tag:
                key = (child.text or "").strip()
            elif child.tag == val_tag:
                val = (child.text or "").strip()
        if key is not None:
            result[key] = val or ""
    return result


def t(elem, tag: str) -> str:
    """Get text of a direct child element, or empty string."""
    child = elem.find(tag)
    return (child.text or "").strip() if child is not None else ""


def parse_prescription(elem: ET.Element, dicts: dict) -> dict:
    row = {}

    # --- flat fields ---
    cod_dcsa = t(elem, "cod_dcsa")
    cod_dcp = t(elem, "cod_dcp")
    cod_dcpf = t(elem, "cod_dcpf")
    cod_envase = t(elem, "cod_envase")
    unid_contenido = t(elem, "unid_contenido")
    lab_tit = t(elem, "laboratorio_titular")
    lab_com = t(elem, "laboratorio_comercializador")
    cod_sitreg = t(elem, "cod_sitreg")
    cod_sitreg_presen = t(elem, "cod_sitreg_presen")

    row["cod_nacion"] = t(elem, "cod_nacion")
    row["nro_definitivo"] = t(elem, "nro_definitivo")
    row["des_nomco"] = t(elem, "des_nomco")
    row["des_prese"] = t(elem, "des_prese")
    row["des_dcsa"] = dicts["dcsa"].get(cod_dcsa, cod_dcsa)
    row["des_dcp"] = dicts["dcp"].get(cod_dcp, cod_dcp)
    row["des_dcpf"] = dicts["dcpf"].get(cod_dcpf, cod_dcpf)
    row["des_dosific"] = t(elem, "des_dosific")
    row["envase"] = dicts["envases"].get(cod_envase, cod_envase)
    row["contenido"] = t(elem, "contenido")
    row["unidad_contenido"] = dicts["unidades"].get(unid_contenido, unid_contenido)
    row["nro_conte"] = t(elem, "nro_conte")
    row["sw_psicotropo"] = t(elem, "sw_psicotropo")
    row["sw_estupefaciente"] = t(elem, "sw_estupefaciente")
    row["sw_afecta_conduccion"] = t(elem, "sw_afecta_conduccion")
    row["sw_triangulo_negro"] = t(elem, "sw_triangulo_negro")
    row["url_fictec"] = t(elem, "url_fictec")
    row["url_prosp"] = t(elem, "url_prosp")
    row["sw_receta"] = t(elem, "sw_receta")
    row["sw_generico"] = t(elem, "sw_generico")
    row["sw_sustituible"] = t(elem, "sw_sustituible")
    row["sw_envase_clinico"] = t(elem, "sw_envase_clinico")
    row["sw_uso_hospitalario"] = t(elem, "sw_uso_hospitalario")
    row["sw_diagnostico_hospitalario"] = t(elem, "sw_diagnostico_hospitalario")
    row["sw_tld"] = t(elem, "sw_tld")
    row["sw_especial_control_medico"] = t(elem, "sw_especial_control_medico")
    row["sw_huerfano"] = t(elem, "sw_huerfano")
    row["sw_base_a_plantas"] = t(elem, "sw_base_a_plantas")
    row["laboratorio_titular"] = dicts["labs"].get(lab_tit, lab_tit)
    row["laboratorio_comercializador"] = dicts["labs"].get(lab_com, lab_com)
    row["fecha_autorizacion"] = t(elem, "fecha_autorizacion")
    row["sw_comercializado"] = t(elem, "sw_comercializado")
    row["fec_comer"] = t(elem, "fec_comer")
    row["situacion_registro"] = dicts["sitreg"].get(cod_sitreg, cod_sitreg)
    row["situacion_registro_presen"] = dicts["sitreg"].get(cod_sitreg_presen, cod_sitreg_presen)
    row["fecha_situacion_registro"] = t(elem, "fecha_situacion_registro")
    row["fec_sitreg_presen"] = t(elem, "fec_sitreg_presen")
    row["sw_tiene_excipientes_decl_obligatoria"] = t(elem, "sw_tiene_excipientes_decl_obligatoria")
    row["biosimilar"] = t(elem, "biosimilar")
    row["importacion_paralela"] = t(elem, "importacion_paralela")
    row["radiofarmaco"] = t(elem, "radiofarmaco")
    row["serializacion"] = t(elem, "serializacion")

    # --- formasfarmaceuticas (nested block) ---
    ff = elem.find("formasfarmaceuticas")
    if ff is not None:
        cod_forfar = t(ff, "cod_forfar")
        cod_forfar_simp = t(ff, "cod_forfar_simplificada")
        row["forma_farmaceutica"] = dicts["forfar"].get(cod_forfar, cod_forfar)
        row["forma_farmaceutica_simplificada"] = dicts["forfar_simp"].get(cod_forfar_simp, cod_forfar_simp)
        row["nro_pactiv"] = t(ff, "nro_pactiv")

        # composicion_pa: one entry per active ingredient, sorted by orden_colacion
        pas = []
        for pa in ff.findall("composicion_pa"):
            cod_pa = t(pa, "cod_principio_activo")
            nombre = dicts["principios"].get(cod_pa, cod_pa)
            dosis = t(pa, "dosis_pa")
            unidad = t(pa, "unidad_dosis_pa")
            orden_raw = t(pa, "orden_colacion")
            try:
                orden = int(orden_raw)
            except ValueError:
                orden = 99  # e.g. "N/A (más de 4 PA)"
            pas.append((orden, f"{nombre} {dosis} {unidad}".strip()))
        pas.sort(key=lambda x: x[0])
        row["principios_activos"] = "|".join(s for _, s in pas)

        # viasadministracion: pipe-separated route names
        vias_list = []
        for va in ff.findall("viasadministracion"):
            cod_via = t(va, "cod_via_admin")
            vias_list.append(dicts["vias"].get(cod_via, cod_via))
        row["vias_administracion"] = "|".join(vias_list)
    else:
        row["forma_farmaceutica"] = ""
        row["forma_farmaceutica_simplificada"] = ""
        row["nro_pactiv"] = ""
        row["principios_activos"] = ""
        row["vias_administracion"] = ""

    # --- atc (single block, duplicidades omitted) ---
    atc_elem = elem.find("atc")
    if atc_elem is not None:
        cod_atc = t(atc_elem, "cod_atc")
        row["cod_atc"] = cod_atc
        row["des_atc"] = dicts["atc"].get(cod_atc, "")
    else:
        row["cod_atc"] = ""
        row["des_atc"] = ""

    return row


def main():
    print(f"Downloading {URL} ...", file=sys.stderr)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data = urllib.request.urlopen(URL, timeout=60, context=ctx).read()
    print(f"Downloaded {len(data):,} bytes", file=sys.stderr)

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        print("Loading dictionaries...", file=sys.stderr)
        dicts = {
            "dcsa":       parse_dict(zf, "DICCIONARIO_DCSA.xml", "codigodcsa", "nombredcsa"),
            "dcp":        parse_dict(zf, "DICCIONARIO_DCP.xml", "codigodcp", "nombredcp"),
            "dcpf":       parse_dict(zf, "DICCIONARIO_DCPF.xml", "codigodcpf", "nombredcpf"),
            "envases":    parse_dict(zf, "DICCIONARIO_ENVASES.xml", "codigoenvase", "envase"),
            "unidades":   parse_dict(zf, "DICCIONARIO_UNIDAD_CONTENIDO.xml", "codigounidadcontenido", "unidadcontenido"),
            "labs":       parse_dict(zf, "DICCIONARIO_LABORATORIOS.xml", "codigolaboratorio", "laboratorio"),
            "sitreg":     parse_dict(zf, "DICCIONARIO_SITUACION_REGISTRO.xml", "codigosituacionregistro", "situacionregistro"),
            "forfar":     parse_dict(zf, "DICCIONARIO_FORMA_FARMACEUTICA.xml", "codigoformafarmaceutica", "formafarmaceutica"),
            "forfar_simp": parse_dict(
                zf,
                "DICCIONARIO_FORMA_FARMACEUTICA_SIMPLIFICADAS.xml",
                "codigoformafarmaceuticasimplificada",
                "formafarmaceuticasimplificada",
            ),
            "principios": parse_dict(zf, "DICCIONARIO_PRINCIPIOS_ACTIVOS.xml", "nroprincipioactivo", "principioactivo"),
            "vias":       parse_dict(zf, "DICCIONARIO_VIAS_ADMINISTRACION.xml", "codigoviaadministracion", "viaadministracion"),
            "atc":        parse_dict(zf, "DICCIONARIO_ATC.xml", "codigoatc", "descatc"),
        }
        for name, d in dicts.items():
            print(f"  {name}: {len(d)} entries", file=sys.stderr)

        print("Parsing Prescripcion.xml...", file=sys.stderr)
        with zf.open("Prescripcion.xml") as f:
            xml_bytes = strip_namespaces(f.read())

    root = ET.fromstring(xml_bytes)
    prescriptions = root.findall("prescription")
    print(f"Found {len(prescriptions):,} prescriptions", file=sys.stderr)

    out_path = OUT_TSV
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=COLUMNS, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for i, p in enumerate(prescriptions):
            row = parse_prescription(p, dicts)
            writer.writerow(row)
            if (i + 1) % 5000 == 0:
                print(f"  {i + 1:,} / {len(prescriptions):,}", file=sys.stderr)

    print(f"Done. Written to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

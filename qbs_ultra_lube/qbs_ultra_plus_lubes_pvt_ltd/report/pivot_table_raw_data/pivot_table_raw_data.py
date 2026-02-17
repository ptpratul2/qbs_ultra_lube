# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.utils.xlsxutils import make_xlsx

def execute(filters=None):
    filters = filters or {}

    # 1. Run your existing SQL query unchanged
    sql = """ 
    SELECT
    r.sample_name AS `Sample Code`,
    i.item_name AS `Sample Name`,
    r.date_and_time_of_sample_receipt AS `Date and Time of Sample Receipt`,
    r.batch_no AS `Batch No.`,
    r.name_of_customer AS `Name of Customer`,
    r.sample_registration_no AS `Sample Registration No.`,
    r.tankervehiclebktankfilling_line_no AS `Tanker/Vehicle/BK/Tank/Filling Line No.`,
    r.tested_by AS `Tested By`,
    r.type_of_sample AS `Type of Sample`,

    /* ===== SEPARATE COLUMNS (AS BEFORE) ===== */
    CASE
        WHEN r.appearance_visual IS NULL OR TRIM(r.appearance_visual) = '' THEN 'NA'
        ELSE r.appearance_visual
    END AS `Appearance (Visual)`,

    CASE
        WHEN r.colour_visual IS NULL OR TRIM(r.colour_visual) = '' THEN 'NA'
        ELSE r.colour_visual
    END AS `Colour (Visual)`,

    p.parameter_name AS `Parameter Name`,
    CASE
        WHEN p.value IS NULL
          OR TRIM(p.value) = ''
          OR LOWER(TRIM(p.value)) = 'na'
        THEN 'NA'
        ELSE p.value
    END AS `Value`

FROM `tabRaw Data Sample` r
LEFT JOIN `tabItem` i
    ON i.item_code = r.sample_name

/* -------------------------
   PARAMETERS (CHILD + FIELDS)
-------------------------- */
INNER JOIN (

    /* ===== CHILD TABLE PARAMETERS ===== */
    SELECT
        rdt.parent AS parent,
        rdt.parameter_name,
        rdt.value
    FROM `tabRaw Data Sample Table` rdt
    WHERE rdt.parameter_name IN (
        'Average KV@ 100°C (four significant figure)',
        'Average KV@ 40°C (four significant figure)',
        'Average Viscosity Blend @ 100°C (four significant figure)',
        'Average KV (Four Significant Figure)',
        'Average Density 15.0C (Four Significant Figure)',
        'Average Density 15.0C (ASTM D1298)',
        'Average Density 20.0C (Four Significant Figure)',
        'Average Density 20.0C (ASTM D1298)',
        'Average Density 29.5C (Four Significant Figure)',
        'Average Density 29.5C (ASTM D1298)',
        'Average Density 15.60C (Four Significant Figure)',
        'Average Density 15.60C (ASTM D1298)',
        'Average Density 15.50C (Four Significant Figure)',
        'Average Density 15.50C (ASTM D1298)',
        'Average Total Base Number',
        'Average Total Acid Number',
        'Average @ 88.0 °C Tendency (T)',
        'Average @ 88.0 °C Stability (S)',
        'Average Air Release',
        'Average Moisture Content',
        'ISO 4406(4 µm/6 µm/14 µm)',
	    'NAS (Class)',
        'SMS 3010',
        'KV@ 100°C',
        'KV@ 40°C',
        'Viscosity Index (ASTM D2270)',
        'Brookfield Viscosity @ -12C (ASTM D2983)',
        'Brookfield Viscosity @-18C (ASTM D2983)',
        'Brookfield Viscosity @ -20C (ASTM D2983)',
        'Brookfield Viscosity @-26C (ASTM D2983)',
        'Brookfield Viscosity @-35C (ASTM D2983)',
        'Brookfield Viscosity @ -40C (ASTM D2983)',
        'Brookfield Viscosity @ -55C (ASTM D2983)',
        'Sequence I @ 24.0°C Result',
        'Sequence II @ 93.5°C Result',
        'Sequence III @ 24.0°C Result',
        'Sequence IV @ 150 °C Result',
        'Result',
        'Reported Pour point (Observed Pour point+3) (Nearest 1°C)',
        'Reported Flash point {C+0.033(760-P)} (Nearest 1°C)',
        'Reported Flash point {C+0.033(760-P)} (Nearest 0.5°C)',
        'Boron',
        'Calcium',
        'Magnesium',
        'Molybdenum',
        'Phosphorus',
        'Zinc',
        'Sulphur',
        'Silicon',
        'Nitrogen',
        'Titanium',
        'Boron (ASTM D5185)',
        'Calcium (ASTM D5185)',
        'Magnesium (ASTM D5185)',
        'Molybdenum (ASTM D5185)',
        'Phosphorus (ASTM D5185)',
        'Zinc (ASTM D5185)',
        'Sulphur (ASTM D5185)',
        'Silicon (ASTM D5185)',
        'Nitrogen (ASTM D5185)',
        'Titanium (ASTM D5185)',
        'Silicon (ASTM D6130)',
        'Silicate (ASTM D6130)',
        'CCS @ -10 (ASTM D5293)',
        'CCS @ -15 (ASTM D5293)',
        'CCS @ -20 (ASTM D5293)',
        'CCS @ -25 (ASTM D5293)',
        'CCS @ -30 (ASTM D5293)',
        'CCS @ -35 (ASTM D5293)',
        'Four Ball Wear Scar (ASTM D4172)',
        'Copper Corrosion (ASTM D130) @ 100°C for 3hrs',
        'Four Ball Weld Load (ASTM D2783)',
        'Water Content (ASTM D6304) (Nearest 1 ppm)',
        'Lubad (LQS025)',
        'Chlorine (ASTM D4927)',
        'KRL after 48 Hrs (ASTM D445) (Four significant figure)',
        'Demulsibility (IP 19)',
        'HTHS @150°C (ASTM D4683)',
        'Noack Volatality (ASTM D5800)',
        'Viscosity, MRV / Yield Stress -10C (ASTM D4684)',
        'Viscosity, MRV / Yield Stress -15C (ASTM D4684)',
        'Viscosity, MRV / Yield Stress -20C (ASTM D4684)',
        'Viscosity, MRV / Yield Stress -25C (ASTM D4684)',
        'Viscosity, MRV / Yield Stress -30C (ASTM D4684)',
        'Viscosity, MRV / Yield Stress -35C (ASTM D4684)',
        'Viscosity, MRV / Yield Stress -40C (ASTM D4684)',
        'Yield Stress, MRV -35C (ASTM D4684)',
        'Yield Stress, MRV -30C (ASTM D4684)',
        'Yield Stress, MRV -20C (ASTM D4684)',
        'Yield Stress, MRV -25C (ASTM D4684)',
        'Filterability (Filterability factor)Stage 1 (Wet)',
        'Filterability (Filterability factor)Stage 1 (Dry)',
        'Filterability (Filterability factor)Stage 2 (Wet)',
        'Filterability (Filterability factor)Stage 2 (Dry)',
        'Filterability 1 st 100 ml,0.8µm (AMS 1082)',
        'Phenolic Inhibitor (AMS 872)',
        'Nitrogen (AMS 1208)',
        'pH - (ASTM D1287)',
        'pH - 50 %% Dil.(ASTM D1287)',
        'pH @25˚C- (ASTM D1287)',
        'pH @25˚C - 50 %% Dil.(ASTM D1287)',
        'pH @25˚C - 30 %% Dil.(ASTM D1287)',
        'pH @25˚C - 33 %% Dil.(ASTM D1287)',
        'pH @25˚C - 10 %% Dil.(ASTM D1287)',
        'pH @25˚C - 20 %% Dil.(ASTM D1287)',
        'pH@25C (ISO 3696)',
        'ERBP  (ASTM D1120) (Nearest 0.3°C)',
        'Wet ERBP (ASTM D1120) (Nearest 0.3°C)',
	    'Reserved Alkalinity',
	    'Reserved Alkalinity 10 ml',
	    'Reserved Alkalinity 10 gm',
        'CA',
        'CP',
        'CN',
        'IBP',
        'FBP',
        'Boiling Point  (ASTM D1120) (Nearest 0.3°C)',
        'Boiling Point 50%% Dil. (ASTM D1120) (Nearest 0.3°C)',
        'Chloride Content   = (BRS-BRBXNormalityX7100)'
    )

    UNION ALL

    /* ===== SINGLE FIELD PARAMETERS (EXCEPT VISUALS) ===== */

SELECT
    name AS parent,
    'Color (ASTM D1500)' AS parameter_name,
    colour_astm_d1500 AS value
FROM `tabRaw Data Sample`
WHERE colour_astm_d1500 IS NOT NULL
  AND TRIM(colour_astm_d1500) != ''
  AND LOWER(TRIM(colour_astm_d1500)) != 'na'

UNION ALL
SELECT name, 'Crackle Test', crackle AS value
FROM `tabRaw Data Sample`
WHERE crackle IS NOT NULL
  AND TRIM(crackle) != ''
  AND LOWER(TRIM(crackle)) != 'na'

UNION ALL
SELECT name, 'Container Sr. No.', container_sr_no AS value
FROM `tabRaw Data Sample`
WHERE container_sr_no IS NOT NULL
  AND TRIM(container_sr_no) != ''
  AND LOWER(TRIM(container_sr_no)) != 'na'

UNION ALL
SELECT name, 'Odour', odour AS value
FROM `tabRaw Data Sample`
WHERE odour IS NOT NULL
  AND TRIM(odour) != ''
  AND LOWER(TRIM(odour)) != 'na'

UNION ALL
SELECT name, 'RPVOT', rpvot AS value
FROM `tabRaw Data Sample`
WHERE rpvot IS NOT NULL
  AND TRIM(rpvot) != ''
  AND LOWER(TRIM(rpvot)) != 'na'

UNION ALL
SELECT name, 'Freezing Point', freezing_point AS value
FROM `tabRaw Data Sample`
WHERE freezing_point IS NOT NULL
  AND TRIM(freezing_point) != ''
  AND LOWER(TRIM(freezing_point)) != 'na'

UNION ALL
SELECT name, 'Freezing Point 50%% Dil.', freezing_point_50_dil AS value
FROM `tabRaw Data Sample`
WHERE freezing_point_50_dil IS NOT NULL
  AND TRIM(freezing_point_50_dil) != ''
  AND LOWER(TRIM(freezing_point_50_dil)) != 'na'

UNION ALL
SELECT name, 'Freezing Point 33%% Dil.', freezing_point_33_dil AS value
FROM `tabRaw Data Sample`
WHERE freezing_point_33_dil IS NOT NULL
  AND TRIM(freezing_point_33_dil) != ''
  AND LOWER(TRIM(freezing_point_33_dil)) != 'na'

UNION ALL
SELECT name, 'Solubility in Water (Inhouse)', solubility_in_water_inhouse AS value
FROM `tabRaw Data Sample`
WHERE solubility_in_water_inhouse IS NOT NULL
  AND TRIM(solubility_in_water_inhouse) != ''
  AND LOWER(TRIM(solubility_in_water_inhouse)) != 'na'

UNION ALL
SELECT name, 'Suspended Matter (Visual)', suspended_matter_visual AS value
FROM `tabRaw Data Sample`
WHERE suspended_matter_visual IS NOT NULL
  AND TRIM(suspended_matter_visual) != ''
  AND LOWER(TRIM(suspended_matter_visual)) != 'na'

UNION ALL
SELECT name, 'Viscosity Index', viscosity_index
FROM `tabRaw Data Sample`
WHERE viscosity_index IS NOT NULL
  AND TRIM(viscosity_index) != ''
  AND LOWER(TRIM(viscosity_index)) != 'na'

UNION ALL
SELECT name, 'KV@-40°C in Cst (ISO 3104)', kv_minus40c_in_cst_iso_3104 AS value
FROM `tabRaw Data Sample`
WHERE kv_minus40c_in_cst_iso_3104 IS NOT NULL
  AND TRIM(kv_minus40c_in_cst_iso_3104) != ''
  AND LOWER(TRIM(kv_minus40c_in_cst_iso_3104)) != 'na'

UNION ALL
SELECT name, 'Viscosity @ 100°C (After 120 shear cycles)', viscosity_100_deg_c_astm_d6278 AS value
FROM `tabRaw Data Sample`
WHERE viscosity_100_deg_c_astm_d6278 IS NOT NULL
  AND TRIM(viscosity_100_deg_c_astm_d6278) != ''
  AND LOWER(TRIM(viscosity_100_deg_c_astm_d6278)) != 'na'

UNION ALL
SELECT name, 'TAN (ASTM D664)', tan_astm_d664 AS value
FROM `tabRaw Data Sample`
WHERE tan_astm_d664 IS NOT NULL
  AND TRIM(tan_astm_d664) != ''
  AND LOWER(TRIM(tan_astm_d664)) != 'na'

UNION ALL
SELECT name, 'Cloud Point', cloud_point AS value
FROM `tabRaw Data Sample`
WHERE cloud_point IS NOT NULL
  AND TRIM(cloud_point) != ''
  AND LOWER(TRIM(cloud_point)) != 'na'

UNION ALL
SELECT name, 'Rust Prevention', rust_preventive_astm_d665b AS value
FROM `tabRaw Data Sample`
WHERE rust_preventive_astm_d665b IS NOT NULL
  AND TRIM(rust_preventive_astm_d665b) != ''
  AND LOWER(TRIM(rust_preventive_astm_d665b)) != 'na'

UNION ALL
SELECT name, 'FTIR', select_hbci AS value
FROM `tabRaw Data Sample`
WHERE select_hbci IS NOT NULL
  AND TRIM(select_hbci) != ''
  AND LOWER(TRIM(select_hbci)) != 'na'

UNION ALL
SELECT name, 'Sulphated Ash', sulphated_ash__wt_astm_d874 AS value
FROM `tabRaw Data Sample`
WHERE sulphated_ash__wt_astm_d874 IS NOT NULL
  AND TRIM(sulphated_ash__wt_astm_d874) != ''
  AND LOWER(TRIM(sulphated_ash__wt_astm_d874)) != 'na'

UNION ALL
SELECT name, 'Ash (ASTM D482)', ash_astm_d482 AS value
FROM `tabRaw Data Sample`
WHERE ash_astm_d482 IS NOT NULL
  AND TRIM(ash_astm_d482) != ''
  AND LOWER(TRIM(ash_astm_d482)) != 'na'

UNION ALL
SELECT name, 'Saponification Value (ASTM D94)', saponification_value_astm_d94 AS value
FROM `tabRaw Data Sample`
WHERE saponification_value_astm_d94 IS NOT NULL
  AND TRIM(saponification_value_astm_d94) != ''
  AND LOWER(TRIM(saponification_value_astm_d94)) != 'na'

UNION ALL
SELECT name, 'Filterability Factor (TMS 371)', filterability_factor_tms_371 AS value
FROM `tabRaw Data Sample`
WHERE filterability_factor_tms_371 IS NOT NULL
  AND TRIM(filterability_factor_tms_371) != ''
  AND LOWER(TRIM(filterability_factor_tms_371)) != 'na'

UNION ALL
SELECT name, 'Total Dissolve Solid (ISO 3696)', total_dissolve_solid__iso_3696 AS value
FROM `tabRaw Data Sample`
WHERE total_dissolve_solid__iso_3696 IS NOT NULL
  AND TRIM(total_dissolve_solid__iso_3696) != ''
  AND LOWER(TRIM(total_dissolve_solid__iso_3696)) != 'na'

UNION ALL
SELECT name, 'Conductivity @ 25°C (ISO 3696)', conductivity_25c_iso_3696 AS value
FROM `tabRaw Data Sample`
WHERE conductivity_25c_iso_3696 IS NOT NULL
  AND TRIM(conductivity_25c_iso_3696) != ''
  AND LOWER(TRIM(conductivity_25c_iso_3696)) != 'na'

UNION ALL
SELECT name, 'Refractive Index', refractive_index AS value
FROM `tabRaw Data Sample`
WHERE refractive_index IS NOT NULL
  AND TRIM(refractive_index) != ''
  AND LOWER(TRIM(refractive_index)) != 'na'

UNION ALL
SELECT name, 'Refractive Index 20°C', refractive_index_20c AS value
FROM `tabRaw Data Sample`
WHERE refractive_index_20c IS NOT NULL
  AND TRIM(refractive_index_20c) != ''
  AND LOWER(TRIM(refractive_index_20c)) != 'na'

UNION ALL
SELECT name, 'Refractive Index @ 20°C (ASTM D1218)', refractive_index__20c_astm_d1218 AS value
FROM `tabRaw Data Sample`
WHERE refractive_index__20c_astm_d1218 IS NOT NULL
  AND TRIM(refractive_index__20c_astm_d1218) != ''
  AND LOWER(TRIM(refractive_index__20c_astm_d1218)) != 'na'

UNION ALL
SELECT name, 'Aniline Point', aniline_point AS value
FROM `tabRaw Data Sample`
WHERE aniline_point IS NOT NULL
  AND TRIM(aniline_point) != ''
  AND LOWER(TRIM(aniline_point)) != 'na'

UNION ALL
SELECT name, 'Sulphur (ASTM D4294)', sulphurastm_d4294 AS value
FROM `tabRaw Data Sample`
WHERE sulphurastm_d4294 IS NOT NULL
  AND TRIM(sulphurastm_d4294) != ''
  AND LOWER(TRIM(sulphurastm_d4294)) != 'na'

UNION ALL
SELECT name, 'Dewatering Property with DM Water', data_riba AS value
FROM `tabRaw Data Sample`
WHERE data_riba IS NOT NULL
  AND TRIM(data_riba) != ''
  AND LOWER(TRIM(data_riba)) != 'na'

UNION ALL
SELECT name, 'Dewatering Property with 3%% NaCl Solution', data_kkzn AS value
FROM `tabRaw Data Sample`
WHERE data_kkzn IS NOT NULL
  AND TRIM(data_kkzn) != ''
  AND LOWER(TRIM(data_kkzn)) != 'na'


) p
    ON p.parent = r.name

/* -------------------------
   FILTERS
-------------------------- */
WHERE
    (%(name_of_customer)s IS NULL OR r.name_of_customer = %(name_of_customer)s)
    AND (%(type_of_sample)s IS NULL OR %(type_of_sample)s = '' OR r.type_of_sample = %(type_of_sample)s)
    AND (%(from_date)s IS NULL OR DATE(r.date_and_time_of_sample_receipt) >= %(from_date)s)
    AND (%(to_date)s IS NULL OR DATE(r.date_and_time_of_sample_receipt) <= %(to_date)s)

ORDER BY
    r.name,
    `Parameter Name`;
    """

    rows = frappe.db.sql(sql, {
        "name_of_customer": filters.get("name_of_customer"),
        "type_of_sample": filters.get("type_of_sample"),
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date")
    }, as_dict=True)

    # 2. Pivot the result
    fixed_fields = [
        "Sample Code", "Sample Name", "Date and Time of Sample Receipt",
        "Batch No.", "Name of Customer", "Sample Registration No.",
        "Tanker/Vehicle/BK/Tank/Filling Line No.", "Tested By",
        "Type of Sample", "Appearance (Visual)", "Colour (Visual)"
    ]
    parameter_names = sorted({row["Parameter Name"] for row in rows})

    grouped = {}
    for row in rows:
        key = tuple(row[field] for field in fixed_fields)
        if key not in grouped:
            grouped[key] = {field: row[field] for field in fixed_fields}
        grouped[key][row["Parameter Name"]] = row["Value"]

    pivoted_rows = list(grouped.values())

    # 3. Build columns for report view
    columns = [{"label": f, "fieldname": f, "fieldtype": "Data"} for f in fixed_fields] + \
              [{"label": p, "fieldname": p, "fieldtype": "Data"} for p in parameter_names]

    return columns, pivoted_rows


# @frappe.whitelist()
# def download_pivoted_excel(filters=None):
#     """Optional: custom endpoint to download Excel directly"""
#     filters = frappe.parse_json(filters) if filters else {}

#     # reuse execute() to get pivoted data
#     columns, data = execute(filters)

#     headers = [col["fieldname"] for col in columns]

#     # Convert dicts to list-of-lists with headers
#     rows = []
#     rows.append(headers)
#     for record in data:
#         row = [record.get(col, "") for col in headers]
#         rows.append(row)

#     xlsx_file = make_xlsx(rows, "Pivoted Report")
#     return frappe.response.download_xlsx(xlsx_file, "pivoted_report.xlsx")

@frappe.whitelist()
def download_pivoted_excel(filters=None):
    filters = frappe.parse_json(filters) if filters else {}

    # reuse execute() to get pivoted data
    columns, data = execute(filters)

    headers = [col["fieldname"] for col in columns]

    # Convert dicts to list-of-lists with headers
    rows = []
    rows.append(headers)
    for record in data:
        row = [record.get(col, "") for col in headers]
        rows.append(row)

    # Generate Excel file in memory
    xlsx_file = make_xlsx(rows, "Pivoted Report")

    # Set response for download
    frappe.response.filename = "pivoted_report.xlsx"
    frappe.response.filecontent = xlsx_file.getvalue()
    frappe.response.type = "binary"
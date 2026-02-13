import { parse } from 'csv-parse/sync';
import db from '../db/database.js';

/**
 * Parse TSV content into array of objects
 * @param {string} tsvContent - TSV file content
 * @param {Array<string>|boolean} columns - Column names or true to use first row
 * @returns {Array<Object>} Parsed rows
 */
function parseTsv(tsvContent, columns) {
  return parse(tsvContent, {
    columns: columns,
    delimiter: '\t',
    skip_empty_lines: true,
    relax_quotes: true,
    relax_column_count: true
  });
}

/**
 * Parse EMA mappings TSV (has header row)
 * Columns: ma_number, concept_id, concept_name, vocabulary_id, concept_code, mapping_type,
 *          ema_active_substance, pdf_strenght, pdf_pharmaceutical_form, pdf_route_of_administration,
 *          pdf_packaging, pdf_content, pdf_pack_size, ema_name_of_medicine, ema_product_number,
 *          ema_atc_code, comment, suggestion, last_updated_date
 */
function parseMappingsTsv(tsvContent) {
  return parseTsv(tsvContent, true);
}

/**
 * Parse product details TSV (has header row)
 */
function parseProductDetailsTsv(tsvContent) {
  return parseTsv(tsvContent, true);
}

/**
 * Clear all existing data from database
 */
function clearDatabase() {
  console.log('Clearing existing data...');

  const tables = [
    'product_countries',
    'market_authorizations',
    'products',
    'product_suppliers',
    'product_brands',
    'product_ingredients',
    'product_groups',
    'source_items'
  ];

  for (const table of tables) {
    db.prepare(`DELETE FROM ${table}`).run();
  }

  console.log('Database cleared');
}

/**
 * Process and insert product data into database
 * @param {Object} data - Object containing mappings and productDetails
 */
export async function processAndStoreData(data) {
  console.log('Processing data...');

  const mappings = parseMappingsTsv(data.mappings);
  const productDetails = parseProductDetailsTsv(data.productDetails);
  const medicinesReport = data.medicinesReport ? parseTsv(data.medicinesReport, true) : [];

  console.log(`Parsed ${mappings.length} mapping records`);
  console.log(`Parsed ${productDetails.length} product detail records`);
  console.log(`Parsed ${medicinesReport.length} medicines report records`);

  // Start transaction
  const transaction = db.transaction(() => {
    clearDatabase();

    // Create lookup maps
    const productDetailsMap = new Map();
    for (const detail of productDetails) {
      const key = detail.ema_product_number;
      if (key) {
        if (!productDetailsMap.has(key)) {
          productDetailsMap.set(key, []);
        }
        productDetailsMap.get(key).push(detail);
      }
    }

    // Create medicines report lookup by EMA product number
    const medicinesReportMap = new Map();
    for (const report of medicinesReport) {
      const key = report['EMA product number'];
      if (key) {
        medicinesReportMap.set(key, report);
      }
    }

    // Group mappings by ema_product_number
    const productGroupsMap = new Map();

    for (const mapping of mappings) {
      const productNumber = mapping.ema_product_number;
      if (!productNumber) continue;

      if (!productGroupsMap.has(productNumber)) {
        productGroupsMap.set(productNumber, {
          mappings: [],
          details: productDetailsMap.get(productNumber) || []
        });
      }

      productGroupsMap.get(productNumber).mappings.push(mapping);
    }

    console.log(`Processing ${productGroupsMap.size} product groups...`);

    // Prepare statements
    const insertProductGroup = db.prepare(`
      INSERT INTO product_groups (
        id, product_number, group_auth_number, name, authorization_holder,
        authorization_holder_country, status, atc_code, therapeutic_group,
        authorisation_date, medicine_url, therapeutic_indication
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    const insertIngredient = db.prepare(`
      INSERT INTO product_ingredients (product_group_id, concept_id, concept_name)
      VALUES (?, ?, ?)
    `);

    const insertBrand = db.prepare(`
      INSERT INTO product_brands (product_group_id, concept_id, concept_name)
      VALUES (?, ?, ?)
    `);

    const insertSupplier = db.prepare(`
      INSERT INTO product_suppliers (product_group_id, concept_id, concept_name)
      VALUES (?, ?, ?)
    `);

    const insertProduct = db.prepare(`
      INSERT INTO products (
        id, product_group_id, product_auth_number, ma_number, name,
        authorisation_holder, strength, pharmaceutical_form, route_of_administration,
        packaging, content, pack_size, concept_id, concept_name
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    let processedCount = 0;

    // Process each product group
    for (const [productNumber, groupData] of productGroupsMap) {
      const mainMapping = groupData.mappings[0];
      const details = groupData.details[0] || {};
      const medicine = medicinesReportMap.get(productNumber) || {};

      const productGroupId = productNumber;

      // Extract name from mapping or details
      const name = mainMapping.ema_name_of_medicine ||
                   details.product_name ||
                   medicine['Name of medicine'] ||
                   mainMapping.concept_name ||
                   'Unknown';

      // Insert product group
      insertProductGroup.run(
        productGroupId,
        productNumber,
        mainMapping.ma_number || details.ma_number || null,
        name,
        medicine['Marketing authorisation developer / applicant / holder'] || null,
        null, // authorization_holder_country - not in source data
        medicine['Medicine status'] || 'Authorised',
        mainMapping.ema_atc_code || medicine['ATC code (human)'] || null,
        null, // therapeutic_group - not in source data
        medicine['Marketing authorisation date'] || null,
        medicine['Medicine URL'] || `https://www.ema.europa.eu/medicines/human/EPAR/${productNumber}`,
        medicine['Therapeutic indication'] || null
      );

      // Insert ingredients from mapping (active substance)
      const ingredients = new Set();
      for (const mapping of groupData.mappings) {
        const ingredientName = mapping.ema_active_substance;
        if (ingredientName && !ingredients.has(ingredientName)) {
          ingredients.add(ingredientName);
          insertIngredient.run(productGroupId, null, ingredientName);
        }
      }

      // Insert brand (from name)
      const brandConceptId = mainMapping.concept_id ? parseInt(mainMapping.concept_id) : null;
      insertBrand.run(productGroupId, brandConceptId, name);

      // Insert supplier (authorization holder)
      const supplierName = medicine['Marketing authorisation developer / applicant / holder'];
      if (supplierName) {
        insertSupplier.run(productGroupId, null, supplierName);
      }

      // Insert individual products from mappings
      for (const mapping of groupData.mappings) {
        const productId = `${productNumber}-${mapping.ma_number || 'default'}-${Math.random().toString(36).substr(2, 9)}`;

        insertProduct.run(
          productId,
          productGroupId,
          mapping.ema_product_number || productNumber,
          mapping.ma_number,
          mainMapping.ema_name_of_medicine || name,
          medicine['Marketing authorisation developer / applicant / holder'] || null,
          mapping.pdf_strenght || null,
          mapping.pdf_pharmaceutical_form || null,
          mapping.pdf_route_of_administration || null,
          mapping.pdf_packaging || null,
          mapping.pdf_content || null,
          mapping.pdf_pack_size || null,
          mapping.concept_id ? parseInt(mapping.concept_id) : null,
          mapping.concept_name || null
        );
      }

      processedCount++;
      if (processedCount % 100 === 0) {
        console.log(`Processed ${processedCount}/${productGroupsMap.size} product groups...`);
      }
    }

    // Update metadata
    db.prepare(`
      INSERT OR REPLACE INTO data_metadata (key, value, updated_at)
      VALUES ('last_update', datetime('now'), datetime('now'))
    `).run();

    console.log(`Successfully processed ${processedCount} product groups`);
  });

  // Execute transaction
  transaction();

  console.log('Data processing complete');
}

/**
 * Get last update timestamp
 * @returns {string|null} Last update timestamp
 */
export function getLastUpdate() {
  const result = db.prepare(`
    SELECT value FROM data_metadata WHERE key = 'last_update'
  `).get();

  return result ? result.value : null;
}

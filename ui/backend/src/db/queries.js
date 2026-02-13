import db from './database.js';

/**
 * Get product groups with pagination, filtering, and search
 * @param {Object} options - Query options
 * @returns {Object} Paginated results
 */
export function getProductGroups(options = {}) {
  const {
    page = 0,
    size = 20,
    search = '',
    status = [],
    authorization_holder_country = [],
    therapeutic_group = [],
    sort = 'product_number,asc'
  } = options;

  const offset = page * size;
  const [sortField, sortOrder] = sort.split(',');

  // Build WHERE clause
  const conditions = [];
  const params = [];

  if (search) {
    conditions.push(`(
      pg.product_number LIKE ? OR
      pg.name LIKE ? OR
      pg.authorization_holder LIKE ? OR
      pg.atc_code LIKE ?
    )`);
    const searchPattern = `%${search}%`;
    params.push(searchPattern, searchPattern, searchPattern, searchPattern);
  }

  if (status && status.length > 0) {
    const placeholders = status.map(() => '?').join(',');
    conditions.push(`pg.status IN (${placeholders})`);
    params.push(...status);
  }

  if (authorization_holder_country && authorization_holder_country.length > 0) {
    const placeholders = authorization_holder_country.map(() => '?').join(',');
    conditions.push(`pg.authorization_holder_country IN (${placeholders})`);
    params.push(...authorization_holder_country);
  }

  if (therapeutic_group && therapeutic_group.length > 0) {
    const placeholders = therapeutic_group.map(() => '?').join(',');
    conditions.push(`pg.therapeutic_group IN (${placeholders})`);
    params.push(...therapeutic_group);
  }

  const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

  // Validate sort field and order
  const validSortFields = ['product_number', 'name', 'atc_code', 'authorization_holder', 'status'];
  const validatedSortField = validSortFields.includes(sortField) ? sortField : 'product_number';
  const validatedSortOrder = sortOrder === 'desc' ? 'DESC' : 'ASC';

  // Get total count
  const countQuery = `SELECT COUNT(*) as total FROM product_groups pg ${whereClause}`;
  const countResult = db.prepare(countQuery).get(...params);
  const total = countResult.total;

  // Get paginated data
  const dataQuery = `
    SELECT
      pg.id,
      pg.product_number,
      pg.group_auth_number,
      pg.name,
      pg.authorization_holder,
      pg.authorization_holder_country,
      pg.status,
      pg.atc_code,
      pg.therapeutic_group,
      pg.authorisation_date,
      pg.refusal_date,
      pg.suspension_date,
      pg.medicine_url,
      pg.therapeutic_indication,
      pg.active_substance_count
    FROM product_groups pg
    ${whereClause}
    ORDER BY pg.${validatedSortField} ${validatedSortOrder}
    LIMIT ? OFFSET ?
  `;

  const groups = db.prepare(dataQuery).all(...params, size, offset);

  // Fetch related data for each group
  for (const group of groups) {
    group.standardized_ingredients = getProductIngredients(group.id);
    group.standardized_brands = getProductBrands(group.id);
    group.standardized_suppliers = getProductSuppliers(group.id);
  }

  return {
    content: groups,
    number: page,
    size: size,
    total_elements: total,
    total_pages: Math.ceil(total / size)
  };
}

/**
 * Get ingredients for a product group
 * @param {string} productGroupId
 * @returns {Array}
 */
function getProductIngredients(productGroupId) {
  const query = `
    SELECT concept_id, concept_name
    FROM product_ingredients
    WHERE product_group_id = ?
  `;

  return db.prepare(query).all(productGroupId);
}

/**
 * Get brands for a product group
 * @param {string} productGroupId
 * @returns {Array}
 */
function getProductBrands(productGroupId) {
  const query = `
    SELECT concept_id, concept_name
    FROM product_brands
    WHERE product_group_id = ?
  `;

  return db.prepare(query).all(productGroupId);
}

/**
 * Get suppliers for a product group
 * @param {string} productGroupId
 * @returns {Array}
 */
function getProductSuppliers(productGroupId) {
  const query = `
    SELECT concept_id, concept_name
    FROM product_suppliers
    WHERE product_group_id = ?
  `;

  return db.prepare(query).all(productGroupId);
}

/**
 * Get products for a specific product group
 * @param {string} productGroupId
 * @returns {Array}
 */
export function getProductsByGroupId(productGroupId) {
  const query = `
    SELECT
      p.id,
      p.product_auth_number,
      p.ma_number,
      p.name,
      p.authorisation_holder,
      p.strength,
      p.pharmaceutical_form,
      p.route_of_administration,
      p.packaging,
      p.content,
      p.pack_size,
      p.concept_id,
      p.concept_name
    FROM products p
    WHERE p.product_group_id = ?
  `;

  const products = db.prepare(query).all(productGroupId);

  // Get country codes for each product
  for (const product of products) {
    product.country_codes = getProductCountries(product.id);
  }

  return products;
}

/**
 * Get country codes for a product
 * @param {string} productId
 * @returns {Array<string>}
 */
function getProductCountries(productId) {
  const query = `
    SELECT country_code
    FROM product_countries
    WHERE product_id = ?
  `;

  const countries = db.prepare(query).all(productId);
  return countries.map(c => c.country_code);
}

/**
 * Get market authorizations for a product group
 * @param {string} productNumber
 * @returns {Array}
 */
export function getMarketAuthorizations(productNumber) {
  const query = `
    SELECT ma_number, source, source_code
    FROM market_authorizations
    WHERE product_group_id = ?
  `;

  const authorizations = db.prepare(query).all(productNumber);

  // Group by MA number
  const grouped = {};
  for (const auth of authorizations) {
    if (!grouped[auth.ma_number]) {
      grouped[auth.ma_number] = {
        ma_number: auth.ma_number,
        items: []
      };
    }

    grouped[auth.ma_number].items.push({
      source: auth.source,
      source_code: auth.source_code
    });
  }

  return Object.values(grouped);
}

/**
 * Get source item details
 * @param {string} source
 * @param {string} sourceCode
 * @returns {Object|null}
 */
export function getSourceItem(source, sourceCode) {
  const query = `
    SELECT data
    FROM source_items
    WHERE source = ? AND source_code = ?
  `;

  const result = db.prepare(query).get(source, sourceCode);

  if (!result) {
    return null;
  }

  return JSON.parse(result.data);
}

/**
 * Get database statistics
 * @returns {Object}
 */
export function getStatistics() {
  const productGroupsCount = db.prepare('SELECT COUNT(*) as count FROM product_groups').get().count;
  const productsCount = db.prepare('SELECT COUNT(*) as count FROM products').get().count;
  const lastUpdate = db.prepare("SELECT value FROM data_metadata WHERE key = 'last_update'").get();

  return {
    product_groups: productGroupsCount,
    products: productsCount,
    last_update: lastUpdate ? lastUpdate.value : null
  };
}

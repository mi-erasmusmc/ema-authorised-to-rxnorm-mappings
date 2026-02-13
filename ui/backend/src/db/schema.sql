-- EMA Product Groups (main table for the product groups)
CREATE TABLE IF NOT EXISTS product_groups (
    id TEXT PRIMARY KEY,
    product_number TEXT NOT NULL,
    group_auth_number TEXT,
    name TEXT NOT NULL,
    authorization_holder TEXT,
    authorization_holder_country TEXT,
    status TEXT,
    atc_code TEXT,
    therapeutic_group TEXT,
    authorisation_date TEXT,
    refusal_date TEXT,
    suspension_date TEXT,
    medicine_url TEXT,
    therapeutic_indication TEXT,
    active_substance_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Standardized Ingredients (active substances) linked to product groups
CREATE TABLE IF NOT EXISTS product_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_group_id TEXT NOT NULL,
    concept_id INTEGER,
    concept_name TEXT NOT NULL,
    FOREIGN KEY (product_group_id) REFERENCES product_groups(id) ON DELETE CASCADE
);

-- Standardized Brands linked to product groups
CREATE TABLE IF NOT EXISTS product_brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_group_id TEXT NOT NULL,
    concept_id INTEGER,
    concept_name TEXT NOT NULL,
    FOREIGN KEY (product_group_id) REFERENCES product_groups(id) ON DELETE CASCADE
);

-- Standardized Suppliers linked to product groups
CREATE TABLE IF NOT EXISTS product_suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_group_id TEXT NOT NULL,
    concept_id INTEGER,
    concept_name TEXT NOT NULL,
    FOREIGN KEY (product_group_id) REFERENCES product_groups(id) ON DELETE CASCADE
);

-- Individual Products (presentations) within a product group
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    product_group_id TEXT NOT NULL,
    product_auth_number TEXT,
    ma_number TEXT,
    name TEXT,
    authorisation_holder TEXT,
    strength TEXT,
    pharmaceutical_form TEXT,
    route_of_administration TEXT,
    packaging TEXT,
    content TEXT,
    pack_size TEXT,
    concept_id INTEGER,
    concept_name TEXT,
    FOREIGN KEY (product_group_id) REFERENCES product_groups(id) ON DELETE CASCADE
);

-- Country codes for products
CREATE TABLE IF NOT EXISTS product_countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    country_code TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Market Authorizations
CREATE TABLE IF NOT EXISTS market_authorizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_group_id TEXT NOT NULL,
    ma_number TEXT NOT NULL,
    source TEXT NOT NULL,
    source_code TEXT NOT NULL,
    FOREIGN KEY (product_group_id) REFERENCES product_groups(id) ON DELETE CASCADE
);

-- Source Items (detailed data from national lists)
CREATE TABLE IF NOT EXISTS source_items (
    source TEXT NOT NULL,
    source_code TEXT NOT NULL,
    data TEXT NOT NULL, -- JSON blob with all source-specific fields
    PRIMARY KEY (source, source_code)
);

-- Metadata table for tracking data updates
CREATE TABLE IF NOT EXISTS data_metadata (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_product_groups_product_number ON product_groups(product_number);
CREATE INDEX IF NOT EXISTS idx_product_groups_atc ON product_groups(atc_code);
CREATE INDEX IF NOT EXISTS idx_product_groups_status ON product_groups(status);
CREATE INDEX IF NOT EXISTS idx_product_groups_country ON product_groups(authorization_holder_country);
CREATE INDEX IF NOT EXISTS idx_product_groups_therapeutic_group ON product_groups(therapeutic_group);
CREATE INDEX IF NOT EXISTS idx_product_groups_name ON product_groups(name);

CREATE INDEX IF NOT EXISTS idx_product_ingredients_group ON product_ingredients(product_group_id);
CREATE INDEX IF NOT EXISTS idx_product_brands_group ON product_brands(product_group_id);
CREATE INDEX IF NOT EXISTS idx_product_suppliers_group ON product_suppliers(product_group_id);

CREATE INDEX IF NOT EXISTS idx_products_group ON products(product_group_id);
CREATE INDEX IF NOT EXISTS idx_products_ma_number ON products(ma_number);

CREATE INDEX IF NOT EXISTS idx_product_countries_product ON product_countries(product_id);

CREATE INDEX IF NOT EXISTS idx_market_auth_group ON market_authorizations(product_group_id);
CREATE INDEX IF NOT EXISTS idx_market_auth_ma_number ON market_authorizations(ma_number);

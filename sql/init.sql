-- Initialize database schema for Databricks metadata replica
-- This schema mirrors the information_schema structure from Databricks

-- Catalogs table
CREATE TABLE IF NOT EXISTS catalogs (
    catalog_name VARCHAR(255) PRIMARY KEY,
    catalog_owner VARCHAR(255),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Schemas table
CREATE TABLE IF NOT EXISTS schemas (
    catalog_name VARCHAR(255),
    schema_name VARCHAR(255),
    schema_owner VARCHAR(255),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (catalog_name, schema_name),
    FOREIGN KEY (catalog_name) REFERENCES catalogs(catalog_name)
);

-- Tables table
CREATE TABLE IF NOT EXISTS tables (
    table_catalog VARCHAR(255),
    table_schema VARCHAR(255),
    table_name VARCHAR(255),
    table_type VARCHAR(50),
    table_owner VARCHAR(255),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (table_catalog, table_schema, table_name),
    FOREIGN KEY (table_catalog, table_schema) REFERENCES schemas(catalog_name, schema_name)
);

-- Columns table
CREATE TABLE IF NOT EXISTS columns (
    table_catalog VARCHAR(255),
    table_schema VARCHAR(255),
    table_name VARCHAR(255),
    column_name VARCHAR(255),
    ordinal_position INTEGER,
    data_type VARCHAR(255),
    is_nullable BOOLEAN,
    column_default TEXT,
    comment TEXT,
    PRIMARY KEY (table_catalog, table_schema, table_name, column_name),
    FOREIGN KEY (table_catalog, table_schema, table_name) REFERENCES tables(table_catalog, table_schema, table_name)
);

-- Create indexes for better query performance
CREATE INDEX idx_tables_catalog_schema ON tables(table_catalog, table_schema);
CREATE INDEX idx_columns_table ON columns(table_catalog, table_schema, table_name);
CREATE INDEX idx_schemas_catalog ON schemas(catalog_name);

-- Insert sample data for testing

-- Sample catalogs
INSERT INTO catalogs (catalog_name, catalog_owner, comment) VALUES
    ('main', 'admin', 'Main production catalog'),
    ('dev', 'dev_team', 'Development catalog'),
    ('analytics', 'analytics_team', 'Analytics catalog');

-- Sample schemas
INSERT INTO schemas (catalog_name, schema_name, schema_owner, comment) VALUES
    ('main', 'default', 'admin', 'Default schema'),
    ('main', 'sales', 'sales_team', 'Sales data schema'),
    ('main', 'customer', 'customer_team', 'Customer data schema'),
    ('dev', 'testing', 'dev_team', 'Testing schema'),
    ('analytics', 'reports', 'analytics_team', 'Reporting schema');

-- Sample tables
INSERT INTO tables (table_catalog, table_schema, table_name, table_type, table_owner, comment) VALUES
    ('main', 'sales', 'orders', 'TABLE', 'sales_team', 'Customer orders table'),
    ('main', 'sales', 'order_items', 'TABLE', 'sales_team', 'Order line items'),
    ('main', 'sales', 'products', 'TABLE', 'sales_team', 'Product catalog'),
    ('main', 'customer', 'customers', 'TABLE', 'customer_team', 'Customer information'),
    ('main', 'customer', 'addresses', 'TABLE', 'customer_team', 'Customer addresses'),
    ('analytics', 'reports', 'sales_summary', 'VIEW', 'analytics_team', 'Sales summary view'),
    ('dev', 'testing', 'test_data', 'TABLE', 'dev_team', 'Test data table');

-- Sample columns
INSERT INTO columns (table_catalog, table_schema, table_name, column_name, ordinal_position, data_type, is_nullable, comment) VALUES
    -- orders table columns
    ('main', 'sales', 'orders', 'order_id', 1, 'BIGINT', false, 'Primary key'),
    ('main', 'sales', 'orders', 'customer_id', 2, 'BIGINT', false, 'Foreign key to customers'),
    ('main', 'sales', 'orders', 'order_date', 3, 'DATE', false, 'Date of order'),
    ('main', 'sales', 'orders', 'total_amount', 4, 'DECIMAL(10,2)', true, 'Total order amount'),
    ('main', 'sales', 'orders', 'status', 5, 'STRING', false, 'Order status'),
    
    -- order_items table columns
    ('main', 'sales', 'order_items', 'item_id', 1, 'BIGINT', false, 'Primary key'),
    ('main', 'sales', 'order_items', 'order_id', 2, 'BIGINT', false, 'Foreign key to orders'),
    ('main', 'sales', 'order_items', 'product_id', 3, 'BIGINT', false, 'Foreign key to products'),
    ('main', 'sales', 'order_items', 'quantity', 4, 'INTEGER', false, 'Item quantity'),
    ('main', 'sales', 'order_items', 'unit_price', 5, 'DECIMAL(10,2)', false, 'Price per unit'),
    
    -- products table columns
    ('main', 'sales', 'products', 'product_id', 1, 'BIGINT', false, 'Primary key'),
    ('main', 'sales', 'products', 'product_name', 2, 'STRING', false, 'Product name'),
    ('main', 'sales', 'products', 'category', 3, 'STRING', true, 'Product category'),
    ('main', 'sales', 'products', 'price', 4, 'DECIMAL(10,2)', false, 'Product price'),
    
    -- customers table columns
    ('main', 'customer', 'customers', 'customer_id', 1, 'BIGINT', false, 'Primary key'),
    ('main', 'customer', 'customers', 'first_name', 2, 'STRING', false, 'Customer first name'),
    ('main', 'customer', 'customers', 'last_name', 3, 'STRING', false, 'Customer last name'),
    ('main', 'customer', 'customers', 'email', 4, 'STRING', true, 'Customer email'),
    ('main', 'customer', 'customers', 'created_at', 5, 'TIMESTAMP', false, 'Account creation date'),
    
    -- addresses table columns
    ('main', 'customer', 'addresses', 'address_id', 1, 'BIGINT', false, 'Primary key'),
    ('main', 'customer', 'addresses', 'customer_id', 2, 'BIGINT', false, 'Foreign key to customers'),
    ('main', 'customer', 'addresses', 'street', 3, 'STRING', false, 'Street address'),
    ('main', 'customer', 'addresses', 'city', 4, 'STRING', false, 'City'),
    ('main', 'customer', 'addresses', 'state', 5, 'STRING', false, 'State'),
    ('main', 'customer', 'addresses', 'zip_code', 6, 'STRING', true, 'Zip code');

-- Create a read-only user for the application
-- This ensures the application can only read data, not modify it
CREATE USER readonly_user WITH PASSWORD 'readonly_pass';
GRANT CONNECT ON DATABASE databricks_metadata TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

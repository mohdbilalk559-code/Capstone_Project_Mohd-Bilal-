-- Seed data loader for SQLite

PRAGMA foreign_keys = ON;

-- Clear existing data so the loader can be run again safely.
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;

-- Load the CSV files.
.mode csv
.import --skip 1 data/customers.csv customers
.import --skip 1 data/products.csv products
.import --skip 1 data/orders.csv orders

-- Convert deliberately blank CSV cells into SQL NULL.
UPDATE orders
SET discount_pct = NULL
WHERE discount_pct = '';

UPDATE orders
SET rating = NULL
WHERE rating = '';

-- Verify row counts.
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers;
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products;
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM orders;

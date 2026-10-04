-- ==========================================
-- Mamaearth Capstone Project
-- Seed data from CSV files
-- ==========================================

-- Clear existing data so the script is re-runnable
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;


-- ==========================================
-- 1. Load Customers
-- ==========================================

LOAD DATA LOCAL INFILE 'Data/CUSTOMER.CSV'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, name, city, city_tier, signup_date, acquisition_source);


-- ==========================================
-- 2. Load Products
-- ==========================================

LOAD DATA LOCAL INFILE 'Data/Product.CSV'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, price);


-- ==========================================
-- 3. Load Orders
-- ==========================================

LOAD DATA LOCAL INFILE 'Data/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, product_id, order_date,
 quantity, discount_pct, payment_method, rating, returned);


-- ==========================================
-- 4. Convert blank numeric values to NULL
-- ==========================================

UPDATE orders
SET discount_pct = NULL
WHERE discount_pct = '';

UPDATE orders
SET rating = NULL
WHERE rating = '';


-- ==========================================
-- 5. Verify loaded records
-- ==========================================

SELECT COUNT(*) AS customer_count FROM customers;

SELECT COUNT(*) AS product_count FROM products;

SELECT COUNT(*) AS order_count FROM orders;

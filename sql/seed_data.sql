SELECT COUNT(*) FROM customers; 
SELECT COUNT(*) FROM products; 
SELECT COUNT(*) FROM orders;   

UPDATE orders SET discount_pct = NULL WHERE discount_pct = '';
UPDATE orders SET rating = NULL WHERE rating = '';

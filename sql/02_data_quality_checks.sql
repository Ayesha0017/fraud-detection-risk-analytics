/*
DATA QUALITY CHECKS
*/

SELECT 
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions;

SELECT 
    ROUND(SUM(amount), 2) AS total_fraud_loss
FROM transactions
WHERE is_fraud = 1;


SELECT COUNT(DISTINCT customer_id) AS total_registered_customers FROM customers;
SELECT COUNT(DISTINCT customer_id) AS total_active_transactors FROM transactions;
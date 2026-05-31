/*

EXECUTIVE FRAUD KPIs

*/


SELECT 
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions;

SELECT 
    ROUND(SUM(amount), 2) AS total_fraud_loss
FROM transactions
WHERE is_fraud = 1;

SELECT TOP 10
    customer_id,
    ROUND(SUM(amount), 2) AS total_fraud_amount
FROM transactions
WHERE is_fraud = 1
GROUP BY customer_id
ORDER BY total_fraud_amount DESC;
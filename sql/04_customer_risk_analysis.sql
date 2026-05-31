/*
CUSTOMER RISK ANALYSIS
*/

SELECT
    c.customer_id,
    c.account_type,
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    ROUND(SUM(t.amount), 2) AS total_spend,
    ROUND(AVG(t.amount), 2) AS avg_transaction
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.account_type,
    c.city
ORDER BY total_spend DESC;

SELECT
    c.account_type,
    COUNT(*) AS total_transactions,
    SUM(t.is_fraud) AS fraud_transactions,
    ROUND(100.0 * SUM(t.is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.account_type
ORDER BY fraud_rate_pct DESC
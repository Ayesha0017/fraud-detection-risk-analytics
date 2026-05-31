/*

MERCHANT / CHANNEL / DEVICE ANALYSIS

*/

USE BankingFraudAnalytics
---

SELECT
    merchant,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY merchant
ORDER BY fraud_rate_pct DESC;

SELECT
    channel,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY channel
ORDER BY fraud_rate_pct DESC;

SELECT
    device_type,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY device_type
ORDER BY fraud_rate_pct DESC


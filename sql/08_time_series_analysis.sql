/*
FRAUD TREND ANALYSIS
*/

WITH daily_fraud AS (
    SELECT
        CAST(transaction_time AS DATE) AS transaction_date,
        COUNT(*) AS total_transactions,
        SUM(CAST(is_fraud AS INT)) AS fraud_transactions
    FROM transactions
    GROUP BY CAST(transaction_time AS DATE)
)
SELECT
    transaction_date,
    total_transactions,
    fraud_transactions,
    ROUND(100.0 * fraud_transactions / total_transactions, 2) AS fraud_rate_pct,
    ROUND(
        AVG(100.0 * fraud_transactions / total_transactions) OVER (
            ORDER BY transaction_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 
        2
    ) AS rolling_7day_fraud_rate
FROM daily_fraud;
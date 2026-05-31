/*
BEHAVIORAL FRAUD ANALYSIS
*/

-- Hour Analysis
SELECT
    hour,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY hour
ORDER BY fraud_rate_pct DESC;


-- Weekday vs Weekend
SELECT
    CASE 
        WHEN day_of_week IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY 
    CASE 
        WHEN day_of_week IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END;
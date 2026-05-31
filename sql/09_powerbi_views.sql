USE BankingFraudAnalytics

-- 1. Customer Risk Summary
CREATE VIEW vw_customer_risk_summary AS
SELECT
    c.customer_id,
    c.city,
    c.account_type,
    c.income,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_spend,
    AVG(t.amount) AS avg_transaction_amount,
    MAX(t.amount) AS max_transaction_amount,
    AVG(t.distance_from_home) AS avg_distance,
    SUM(CAST(t.is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(t.is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.city,
    c.account_type,
    c.income

SELECT * FROM vw_customer_risk_summary

-- 2. Merchant Risk Summary
CREATE VIEW vw_merchant_risk AS
SELECT
    merchant,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY merchant

-- 3. Channel Risk Summary
CREATE VIEW vw_channel_risk AS
SELECT
    channel,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY channel

-- 4. Device Risk Summary
CREATE VIEW vw_device_risk AS
SELECT
    device_type,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY device_type

-- 5. Hourly Fraud Pattern (Heatmap Source)
CREATE VIEW vw_hourly_fraud AS
SELECT
    hour,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY hour

-- 6. Daily Fraud Trend (Line Chart Source)
CREATE VIEW vw_daily_fraud_trend AS
SELECT
    CAST(transaction_time AS DATE) AS transaction_date,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    SUM(CASE WHEN CAST(is_fraud AS INT) = 1 THEN amount ELSE 0 END) AS fraud_loss
FROM transactions
GROUP BY CAST(transaction_time AS DATE)

-- 7. Geographic Risk
CREATE VIEW vw_location_risk AS
SELECT
    location,
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(100.0 * SUM(CAST(is_fraud AS INT)) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY location

-- 8. Transaction Velocity
CREATE VIEW vw_transaction_velocity AS
WITH txn_velocity AS (
    SELECT
        customer_id,
        transaction_id,
        transaction_time,
        LAG(transaction_time) OVER (
            PARTITION BY customer_id
            ORDER BY transaction_time
        ) AS previous_transaction_time
    FROM transactions
)
SELECT
    customer_id,
    transaction_id,
    transaction_time,
    DATEDIFF(MINUTE, previous_transaction_time, transaction_time) AS minutes_between_transactions
FROM txn_velocity
WHERE previous_transaction_time IS NOT NULL

-- 9. Fraud Loss Contribution (Executive Dashboard Metric)
CREATE VIEW vw_fraud_loss_contribution AS
SELECT
    customer_id,
    SUM(amount) AS fraud_amount
FROM transactions
WHERE is_fraud = 1
GROUP BY customer_id


CREATE VIEW vw_risk_segment_summary AS
SELECT
    risk_segment,
    COUNT(*) AS transactions,
    AVG(risk_score) AS avg_risk_score,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(
        100.0 * SUM(CAST(is_fraud AS INT))
        / COUNT(*),
        2
    ) AS fraud_rate_pct
FROM transactions
GROUP BY risk_segment

CREATE VIEW vw_fraud_overview AS
SELECT
    COUNT(*) AS total_transactions,
    SUM(CAST(is_fraud AS INT)) AS fraud_transactions,
    ROUND(
        100.0 * SUM(CAST(is_fraud AS INT))
        / COUNT(*),
        2
    ) AS fraud_rate_pct,
    SUM(
        CASE
            WHEN is_fraud = 1 THEN amount
            ELSE 0
        END
    ) AS fraud_loss,
    AVG(
        CASE
            WHEN is_fraud = 1 THEN amount
        END
    ) AS avg_fraud_amount
FROM transactions
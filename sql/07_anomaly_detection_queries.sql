/*
ANOMALY DETECTION QUERIES
*/

-- High Amount Transactions
SELECT TOP 20
    transaction_id,
    customer_id,
    amount,
    merchant,
    channel,
    transaction_time
FROM transactions
ORDER BY amount DESC;

-------------------------------------------------

-- Distance Anomalies
SELECT TOP 20
    transaction_id,
    customer_id,
    amount,
    location,
    distance_from_home,
    is_fraud
FROM transactions
ORDER BY distance_from_home DESC;

-------------------------------------------------

-- Velocity Analysis
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
SELECT TOP 50
    customer_id,
    transaction_id,
    DATEDIFF(MINUTE, previous_transaction_time, transaction_time) AS minutes_between_transactions
FROM txn_velocity
WHERE previous_transaction_time IS NOT NULL
ORDER BY minutes_between_transactions;
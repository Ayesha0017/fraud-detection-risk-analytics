/*
BANKING FRAUD DETECTION PROJECT
Database Setup & Optimization
*/

USE BankingFraudAnalytics;
GO

EXEC sp_help customers;
EXEC sp_help transactions;
EXEC sp_help cards;

/*
Performance Optimization
*/

CREATE INDEX idx_transactions_customer
ON transactions(customer_id);

CREATE INDEX idx_transactions_time
ON transactions(transaction_time);

CREATE INDEX idx_transactions_fraud
ON transactions(is_fraud);

/*
Row Counts
*/

SELECT COUNT(*) AS customers FROM customers;

SELECT COUNT(*) AS transactions FROM transactions;

SELECT COUNT(*) AS cards FROM cards;
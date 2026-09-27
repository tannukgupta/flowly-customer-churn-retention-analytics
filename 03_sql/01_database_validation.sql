#row counts
USE flowly_churn;

SHOW TABLES;

SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'subscriptions', COUNT(*)
FROM subscriptions

UNION ALL

SELECT 'transactions', COUNT(*)
FROM transactions

UNION ALL

SELECT 'customer_activity', COUNT(*)
FROM customer_activity

UNION ALL

SELECT 'support_tickets', COUNT(*)
FROM support_tickets

UNION ALL

SELECT 'marketing_interactions', COUNT(*)
FROM marketing_interactions

UNION ALL

SELECT 'churn_events', COUNT(*)
FROM churn_events;


#Check customer relationships
SELECT COUNT(*) AS orphan_subscriptions
FROM subscriptions s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS orphan_transactions
FROM transactions t
LEFT JOIN customers c
    ON t.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS orphan_activity
FROM customer_activity a
LEFT JOIN customers c
    ON a.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

#Check subscription logic
SELECT
    status,
    COUNT(*) AS subscription_count
FROM subscriptions
GROUP BY status
ORDER BY subscription_count DESC;

SELECT COUNT(*) AS invalid_active_subscriptions
FROM subscriptions
WHERE status = 'Active'
  AND end_date IS NOT NULL;
  
  SELECT COUNT(*) AS invalid_cancelled_subscriptions
FROM subscriptions
WHERE status = 'Cancelled'
  AND end_date IS NULL;
  
#Check transaction status
  SELECT
    transaction_status,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY transaction_status
ORDER BY transaction_count DESC;

SELECT COUNT(*) AS invalid_statuses
FROM transactions
WHERE transaction_status NOT IN ('Successful', 'Failed');

#Check churn
SELECT
    churn_type,
    COUNT(*) AS churn_count
FROM churn_events
GROUP BY churn_type;

SELECT
    churn_reason,
    COUNT(*) AS churn_count
FROM churn_events
GROUP BY churn_reason
ORDER BY churn_count DESC;

#Check support data
SELECT
    COUNT(*) AS total_tickets,
    COUNT(satisfaction_score) AS tickets_with_score,
    COUNT(*) - COUNT(satisfaction_score) AS missing_scores
FROM support_tickets;

#Check the central customer population
SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM customers;
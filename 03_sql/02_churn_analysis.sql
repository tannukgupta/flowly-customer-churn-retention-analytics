
#Analysis 1 — How many customers does Flowly have, and how many have churned?
SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT ce.customer_id) AS churned_customers,
    ROUND(
        COUNT(DISTINCT ce.customer_id) * 100.0
        / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customers c
LEFT JOIN churn_events ce
    ON c.customer_id = ce.customer_id;
    
#Analysis 2 — Does churn vary across plans?
SELECT
    s.plan,
    COUNT(DISTINCT s.customer_id) AS total_customers,
    COUNT(DISTINCT ce.customer_id) AS churned_customers,
    ROUND(
        COUNT(DISTINCT ce.customer_id) * 100.0
        / COUNT(DISTINCT s.customer_id),
        2
    ) AS churn_rate_percent
FROM subscriptions s
LEFT JOIN churn_events ce
    ON s.customer_id = ce.customer_id
GROUP BY s.plan
ORDER BY churn_rate_percent DESC;

#Analysis 3 — Are customers acquired through different channels showing different churn rates?
SELECT
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT ce.customer_id) AS churned_customers,
    ROUND(
        COUNT(DISTINCT ce.customer_id) * 100.0
        / COUNT(DISTINCT c.customer_id),
        2
    ) AS churn_rate_percent
FROM customers c
LEFT JOIN churn_events ce
    ON c.customer_id = ce.customer_id
GROUP BY c.acquisition_channel
ORDER BY churn_rate_percent DESC;

#Analysis 4 — Does customer company size appear to be associated with different churn rates?
SELECT
    c.company_size,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT ce.customer_id) AS churned_customers,
    ROUND(
        COUNT(DISTINCT ce.customer_id) * 100.0
        / COUNT(DISTINCT c.customer_id),
        2
    ) AS churn_rate_percent
FROM customers c
LEFT JOIN churn_events ce
    ON c.customer_id = ce.customer_id
GROUP BY c.company_size
ORDER BY churn_rate_percent DESC;

#Analysis 5 — Churn by customer type
SELECT
    c.customer_type,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT ce.customer_id) AS churned_customers,
    ROUND(
        COUNT(DISTINCT ce.customer_id) * 100.0
        / COUNT(DISTINCT c.customer_id),
        2
    ) AS churn_rate_percent
FROM customers c
LEFT JOIN churn_events ce
    ON c.customer_id = ce.customer_id
GROUP BY c.customer_type
ORDER BY churn_rate_percent DESC;

#Analysis 6 — Why are customers churning?
SELECT
    churn_reason,
    COUNT(*) AS churned_customers,
    ROUND(
        COUNT(*) * 100.0
        / (SELECT COUNT(*) FROM churn_events),
        2
    ) AS percentage_of_churn
FROM churn_events
GROUP BY churn_reason
ORDER BY churned_customers DESC;

#Analysis 7 — Voluntary vs involuntary churn
SELECT
    churn_type,
    COUNT(*) AS churned_customers,
    ROUND(
        COUNT(*) * 100.0
        / (SELECT COUNT(*) FROM churn_events),
        2
    ) AS percentage_of_churn
FROM churn_events
GROUP BY churn_type
ORDER BY churned_customers DESC;
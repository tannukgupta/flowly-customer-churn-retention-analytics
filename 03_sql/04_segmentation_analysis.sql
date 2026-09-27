USE flowly_churn;

#Churn by plan
SELECT
    plan,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_analytical
GROUP BY plan
ORDER BY churn_rate_percent DESC;

#Churn by acquisition channel
SELECT
    acquisition_channel,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_analytical
GROUP BY acquisition_channel
ORDER BY churn_rate_percent DESC;

#Churn by company size
SELECT
    company_size,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_analytical
GROUP BY company_size
ORDER BY churn_rate_percent DESC;

#Churn by customer type
SELECT
    customer_type,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_analytical
GROUP BY customer_type
ORDER BY churn_rate_percent DESC;

#Churn by country
SELECT
    country,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_analytical
GROUP BY country
ORDER BY churn_rate_percent DESC;

#Usage vs churn
SELECT
    CASE
        WHEN total_sessions < 20 THEN 'Low Usage'
        WHEN total_sessions < 50 THEN 'Medium Usage'
        ELSE 'High Usage'
    END AS usage_segment,

    COUNT(*) AS total_customers,

    SUM(churned) AS churned_customers,

    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent

FROM customer_analytical

GROUP BY
    CASE
        WHEN total_sessions < 20 THEN 'Low Usage'
        WHEN total_sessions < 50 THEN 'Medium Usage'
        ELSE 'High Usage'
    END

ORDER BY churn_rate_percent DESC;

#Support-ticket segment
SELECT
    CASE
        WHEN total_support_tickets = 0 THEN 'No Tickets'
        WHEN total_support_tickets <= 2 THEN 'Low Support'
        WHEN total_support_tickets <= 5 THEN 'Medium Support'
        ELSE 'High Support'
    END AS support_segment,

    COUNT(*) AS total_customers,

    SUM(churned) AS churned_customers,

    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent

FROM customer_analytical

GROUP BY
    CASE
        WHEN total_support_tickets = 0 THEN 'No Tickets'
        WHEN total_support_tickets <= 2 THEN 'Low Support'
        WHEN total_support_tickets <= 5 THEN 'Medium Support'
        ELSE 'High Support'
    END

ORDER BY churn_rate_percent DESC;

#Support-ticket segment
SELECT
    CASE
        WHEN total_support_tickets = 0 THEN 'No Tickets'
        WHEN total_support_tickets <= 2 THEN 'Low Support'
        WHEN total_support_tickets <= 5 THEN 'Medium Support'
        ELSE 'High Support'
    END AS support_segment,

    COUNT(*) AS total_customers,

    SUM(churned) AS churned_customers,

    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent

FROM customer_analytical

GROUP BY
    CASE
        WHEN total_support_tickets = 0 THEN 'No Tickets'
        WHEN total_support_tickets <= 2 THEN 'Low Support'
        WHEN total_support_tickets <= 5 THEN 'Medium Support'
        ELSE 'High Support'
    END

ORDER BY churn_rate_percent DESC;

#High-value customers and churn
SELECT
    CASE
        WHEN total_revenue < 100 THEN 'Low Revenue'
        WHEN total_revenue < 500 THEN 'Medium Revenue'
        ELSE 'High Revenue'
    END AS revenue_segment,

    COUNT(*) AS total_customers,

    SUM(churned) AS churned_customers,

    ROUND(
        SUM(churned) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percent,

    ROUND(
        SUM(total_revenue),
        2
    ) AS total_revenue

FROM customer_analytical

GROUP BY
    CASE
        WHEN total_revenue < 100 THEN 'Low Revenue'
        WHEN total_revenue < 500 THEN 'Medium Revenue'
        ELSE 'High Revenue'
    END

ORDER BY churn_rate_percent DESC;

#Revenue at risk
SELECT
    COUNT(*) AS churned_customers,

    ROUND(
        SUM(monthly_price),
        2
    ) AS monthly_recurring_revenue_at_risk

FROM customer_analytical

WHERE churned = 1;

#Voluntary vs involuntary churn + revenue
SELECT
    churn_type,

    COUNT(*) AS churned_customers,

    ROUND(
        SUM(monthly_price),
        2
    ) AS monthly_revenue_associated

FROM customer_analytical

WHERE churned = 1

GROUP BY churn_type;

#Find potentially high-risk customers
SELECT
    customer_id,
    plan,
    monthly_price,
    total_sessions,
    total_support_tickets,
    failed_transactions,
    avg_satisfaction_score,
    churned,

    CASE
        WHEN total_sessions < 20
             AND failed_transactions > 0
             AND total_support_tickets >= 3
        THEN 'Multiple Risk Signals'

        WHEN total_sessions < 20
        THEN 'Low Usage Signal'

        WHEN failed_transactions > 0
        THEN 'Payment Failure Signal'

        WHEN total_support_tickets >= 3
        THEN 'High Support Volume Signal'

        ELSE 'No Strong Signal'
    END AS risk_signal

FROM customer_analytical;
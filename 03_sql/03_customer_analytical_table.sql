USE flowly_churn;

DROP TABLE IF EXISTS customer_analytical;

CREATE TABLE customer_analytical AS

WITH

-- ============================================================
-- CUSTOMER BASE
-- ============================================================

customer_base AS (
    SELECT
        customer_id,
        signup_date,
        age_group,
        country,
        company_size,
        acquisition_channel,
        customer_type
    FROM customers
),


-- ============================================================
-- SUBSCRIPTION FEATURES
-- ============================================================

subscription_features AS (
    SELECT
        customer_id,
        MAX(plan) AS plan,
        MAX(billing_cycle) AS billing_cycle,
        MAX(monthly_price) AS monthly_price,
        MAX(status) AS subscription_status,
        MIN(start_date) AS subscription_start_date,
        MAX(end_date) AS subscription_end_date
    FROM subscriptions
    GROUP BY customer_id
),


-- ============================================================
-- TRANSACTION FEATURES
-- ============================================================

transaction_features AS (
    SELECT
        customer_id,

        COUNT(*) AS total_transactions,

        SUM(
            CASE
                WHEN transaction_status = 'Successful'
                THEN 1
                ELSE 0
            END
        ) AS successful_transactions,

        SUM(
            CASE
                WHEN transaction_status = 'Failed'
                THEN 1
                ELSE 0
            END
        ) AS failed_transactions,

        SUM(
            CASE
                WHEN transaction_status = 'Successful'
                THEN amount
                ELSE 0
            END
        ) AS total_revenue,

        AVG(
            CASE
                WHEN transaction_status = 'Successful'
                THEN amount
            END
        ) AS avg_successful_transaction_amount,

        MAX(transaction_date) AS last_transaction_date

    FROM transactions
    GROUP BY customer_id
),


-- ============================================================
-- ACTIVITY FEATURES
-- ============================================================

activity_features AS (
    SELECT
        customer_id,

        COUNT(*) AS activity_records,

        SUM(sessions) AS total_sessions,

        SUM(session_minutes) AS total_session_minutes,

        SUM(projects_created) AS total_projects_created,

        SUM(files_uploaded) AS total_files_uploaded,

        SUM(features_used) AS total_features_used,

        SUM(active_days) AS total_active_days,

        AVG(sessions) AS avg_sessions_per_activity,

        AVG(session_minutes) AS avg_session_minutes_per_activity

    FROM customer_activity
    GROUP BY customer_id
),


-- ============================================================
-- SUPPORT FEATURES
-- ============================================================

support_features AS (
    SELECT
        customer_id,

        COUNT(*) AS total_support_tickets,

        SUM(
            CASE
                WHEN resolved = 'Yes'
                THEN 1
                ELSE 0
            END
        ) AS resolved_tickets,

        AVG(resolution_hours) AS avg_resolution_hours,

        AVG(satisfaction_score) AS avg_satisfaction_score,

        MAX(ticket_date) AS last_support_ticket_date

    FROM support_tickets
    GROUP BY customer_id
),


-- ============================================================
-- MARKETING FEATURES
-- ============================================================

marketing_features AS (
    SELECT
        customer_id,

        COUNT(*) AS total_marketing_interactions,

        COUNT(DISTINCT campaign_id) AS campaigns_interacted,

        COUNT(
            DISTINCT channel
        ) AS marketing_channels_used,

        MAX(interaction_date) AS last_marketing_interaction_date

    FROM marketing_interactions
    GROUP BY customer_id
),


-- ============================================================
-- CHURN FEATURES
-- ============================================================

churn_features AS (
    SELECT
        customer_id,

        1 AS churned,

        MAX(churn_date) AS churn_date,

        MAX(churn_reason) AS churn_reason,

        MAX(churn_type) AS churn_type

    FROM churn_events
    GROUP BY customer_id
)


-- ============================================================
-- FINAL CUSTOMER-LEVEL DATASET
-- ============================================================

SELECT

    c.customer_id,
    c.signup_date,
    c.age_group,
    c.country,
    c.company_size,
    c.acquisition_channel,
    c.customer_type,

    s.plan,
    s.billing_cycle,
    s.monthly_price,
    s.subscription_status,
    s.subscription_start_date,
    s.subscription_end_date,

    COALESCE(t.total_transactions, 0)
        AS total_transactions,

    COALESCE(t.successful_transactions, 0)
        AS successful_transactions,

    COALESCE(t.failed_transactions, 0)
        AS failed_transactions,

    COALESCE(t.total_revenue, 0)
        AS total_revenue,

    COALESCE(t.avg_successful_transaction_amount, 0)
        AS avg_successful_transaction_amount,

    t.last_transaction_date,

    COALESCE(a.activity_records, 0)
        AS activity_records,

    COALESCE(a.total_sessions, 0)
        AS total_sessions,

    COALESCE(a.total_session_minutes, 0)
        AS total_session_minutes,

    COALESCE(a.total_projects_created, 0)
        AS total_projects_created,

    COALESCE(a.total_files_uploaded, 0)
        AS total_files_uploaded,

    COALESCE(a.total_features_used, 0)
        AS total_features_used,

    COALESCE(a.total_active_days, 0)
        AS total_active_days,

    COALESCE(a.avg_sessions_per_activity, 0)
        AS avg_sessions_per_activity,

    COALESCE(a.avg_session_minutes_per_activity, 0)
        AS avg_session_minutes_per_activity,

    COALESCE(sp.total_support_tickets, 0)
        AS total_support_tickets,

    COALESCE(sp.resolved_tickets, 0)
        AS resolved_tickets,

    COALESCE(sp.avg_resolution_hours, 0)
        AS avg_resolution_hours,

    sp.avg_satisfaction_score,

    sp.last_support_ticket_date,

    COALESCE(m.total_marketing_interactions, 0)
        AS total_marketing_interactions,

    COALESCE(m.campaigns_interacted, 0)
        AS campaigns_interacted,

    COALESCE(m.marketing_channels_used, 0)
        AS marketing_channels_used,

    m.last_marketing_interaction_date,

    COALESCE(ch.churned, 0)
        AS churned,

    ch.churn_date,
    ch.churn_reason,
    ch.churn_type

FROM customer_base c

LEFT JOIN subscription_features s
    ON c.customer_id = s.customer_id

LEFT JOIN transaction_features t
    ON c.customer_id = t.customer_id

LEFT JOIN activity_features a
    ON c.customer_id = a.customer_id

LEFT JOIN support_features sp
    ON c.customer_id = sp.customer_id

LEFT JOIN marketing_features m
    ON c.customer_id = m.customer_id

LEFT JOIN churn_features ch
    ON c.customer_id = ch.customer_id;
    
#checking    
    SELECT COUNT(*) AS customer_rows
FROM customer_analytical;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM customer_analytical;

#Inspect the resulting dataset
SELECT *
FROM customer_analytical
LIMIT 10;

#calculation

#Revenue by churn status
SELECT
    churned,
    COUNT(*) AS customers,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS avg_revenue_per_customer
FROM customer_analytical
GROUP BY churned;

#Average product usage by churn status
SELECT
    churned,
    COUNT(*) AS customers,
    ROUND(AVG(total_sessions), 2) AS avg_sessions,
    ROUND(AVG(total_session_minutes), 2) AS avg_session_minutes,
    ROUND(AVG(total_projects_created), 2) AS avg_projects,
    ROUND(AVG(total_active_days), 2) AS avg_active_days
FROM customer_analytical
GROUP BY churned;

#Support experience by churn status
SELECT
    churned,
    COUNT(*) AS customers,
    ROUND(AVG(total_support_tickets), 2) AS avg_support_tickets,
    ROUND(AVG(avg_resolution_hours), 2) AS avg_resolution_hours,
    ROUND(AVG(avg_satisfaction_score), 2) AS avg_satisfaction_score
FROM customer_analytical
GROUP BY churned;

#Payment failures and churn
SELECT
    churned,
    COUNT(*) AS customers,
    ROUND(AVG(failed_transactions), 2) AS avg_failed_transactions,
    ROUND(
        AVG(
            CASE
                WHEN failed_transactions > 0 THEN 1
                ELSE 0
            END
        ) * 100,
        2
    ) AS pct_with_payment_failure
FROM customer_analytical
GROUP BY churned;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM customer_analytical;
-- ============================================================
-- FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS
-- DATABASE SCHEMA
-- ============================================================


-- Create database
CREATE DATABASE IF NOT EXISTS flowly_churn;

USE flowly_churn;


-- ============================================================
-- 1. CUSTOMERS
-- ============================================================

DROP TABLE IF EXISTS churn_events;
DROP TABLE IF EXISTS marketing_interactions;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS customer_activity;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS customers;


CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE,
    age_group VARCHAR(30),
    country VARCHAR(100),
    company_size VARCHAR(30),
    acquisition_channel VARCHAR(50),
    customer_type VARCHAR(50)
);


-- ============================================================
-- 2. SUBSCRIPTIONS
-- ============================================================

CREATE TABLE subscriptions (
    subscription_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    plan VARCHAR(50),
    start_date DATE,
    end_date DATE NULL,
    billing_cycle VARCHAR(30),
    monthly_price DECIMAL(10,2),
    status VARCHAR(30),

    CONSTRAINT fk_subscription_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 3. TRANSACTIONS
-- ============================================================

CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    transaction_date DATE,
    amount DECIMAL(12,2),
    payment_method VARCHAR(50),
    transaction_status VARCHAR(30),

    CONSTRAINT fk_transaction_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 4. CUSTOMER ACTIVITY
-- ============================================================

CREATE TABLE customer_activity (
    activity_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    activity_date DATE,
    sessions INT,
    session_minutes INT,
    projects_created INT,
    files_uploaded INT,
    features_used INT,
    active_days INT,

    CONSTRAINT fk_activity_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 5. SUPPORT TICKETS
-- ============================================================

CREATE TABLE support_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    ticket_date DATE,
    issue_type VARCHAR(100),
    resolution_hours INT,
    satisfaction_score DECIMAL(3,1) NULL,
    resolved VARCHAR(20),

    CONSTRAINT fk_support_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 6. MARKETING INTERACTIONS
-- ============================================================

CREATE TABLE marketing_interactions (
    interaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    campaign_id VARCHAR(30),
    channel VARCHAR(50),
    interaction_date DATE,
    interaction_type VARCHAR(50),

    CONSTRAINT fk_marketing_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 7. CHURN EVENTS
-- ============================================================

CREATE TABLE churn_events (
    churn_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    churn_date DATE,
    churn_reason VARCHAR(100),
    churn_type VARCHAR(30),

    CONSTRAINT fk_churn_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- VERIFY TABLES
-- ============================================================

SHOW TABLES;
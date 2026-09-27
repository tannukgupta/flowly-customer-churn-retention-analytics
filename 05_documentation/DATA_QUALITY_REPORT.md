# Flowly Customer Churn & Retention Analytics
## Data Quality Report

**Project:** Flowly Customer Churn & Retention Analytics  
**Stage:** Raw Data Quality Investigation  
**Status:** Completed

---

# 1. Objective

The objective of this data quality investigation was to assess the
completeness, consistency, uniqueness, and relational integrity of the
raw Flowly customer datasets before performing analytical work.

The investigation was performed using Python and Pandas.

---

# 2. Tables Audited

The following seven raw datasets were audited:

1. customers
2. subscriptions
3. transactions
4. customer_activity
5. support_tickets
6. marketing_interactions
7. churn_events

---

# 3. Primary Key Validation

All seven tables were checked for duplicate primary-key values.

| Table | Primary Key | Duplicate Records |
|---|---|---:|
| customers | customer_id | 0 |
| subscriptions | subscription_id | 0 |
| transactions | transaction_id | 0 |
| customer_activity | activity_id | 0 |
| support_tickets | ticket_id | 0 |
| marketing_interactions | interaction_id | 0 |
| churn_events | churn_id | 0 |

### Result

All primary-key validation checks passed.

Each record has a unique identifier within its respective table.

---

# 4. Referential Integrity

All child tables containing customer_id were checked against
the customers master table.

| Table | Orphan Customer IDs |
|---|---:|
| subscriptions | 0 |
| transactions | 0 |
| customer_activity | 0 |
| support_tickets | 0 |
| marketing_interactions | 0 |
| churn_events | 0 |

### Result

No orphan customer records were identified.

The customer relationships across the datasets are therefore
structurally consistent.

---

# 5. Missing Value Analysis

## Customers

18 customer records have a missing country value.

This represents approximately 0.18% of the customer population.

### Planned treatment

These records will not be deleted.

The missing country values will be handled during the cleaning stage
using a documented approach.

---

## Subscriptions

8,097 subscription records have a missing end_date.

This was investigated using subscription status.

Validation showed:

- Active subscriptions with an end date: 0
- Cancelled subscriptions without an end date: 0

### Decision

The missing end_date values are considered logically valid for
active subscriptions because an ongoing subscription does not have
a termination date.

These NULL values will therefore be retained.

---

## Support Tickets

20 support ticket records have a missing satisfaction_score.

Validation found:

- Invalid satisfaction scores: 0
- Negative resolution hours: 0

### Planned treatment

The missing satisfaction scores will be investigated before
deciding whether they should remain NULL or be handled for specific
analytical calculations.

---

# 6. Business Duplicate Analysis

Exact duplicate-row detection returned zero duplicates.

However, a business-key duplicate investigation was performed on
customer_activity using:

- customer_id
- activity_date
- sessions
- session_minutes
- projects_created
- files_uploaded
- features_used
- active_days

The investigation identified:

- 25 duplicate business groups
- 50 rows involved in those groups

### Decision

These records will be investigated and handled during the
data-cleaning stage.

The original records will remain unchanged in the raw dataset.

---

# 7. Transaction Validation

The following transaction rules were tested:

- Transaction amount must not be negative.
- Transaction status must belong to the permitted status set.

Results:

- Negative transaction amounts: 0
- Invalid transaction statuses: 0

### Result

Transaction validation passed.

---

# 8. Customer Activity Validation

The following rules were tested:

- Sessions must be at least 1.
- Session minutes cannot be negative.
- Projects created cannot be negative.
- Files uploaded cannot be negative.
- Features used must be at least 1.

All validation checks returned zero invalid records.

### Result

Customer activity passed the basic numerical business-rule checks.

---

# 9. Subscription Logic Validation

The following business rules were tested:

1. Active subscriptions should not have an end date.
2. Cancelled subscriptions should have an end date.

Results:

- Active subscriptions with end date: 0
- Cancelled subscriptions without end date: 0

### Result

Subscription status and date logic are internally consistent.

---

# 10. Churn Validation

The churn table contains 1,903 churn events.

Churn types:

| Churn Type | Records |
|---|---:|
| Voluntary | 1,583 |
| Involuntary | 320 |

No repeated churn events were identified for the same customer.

The recorded churn reasons include:

- Low Usage
- Payment Failure
- Poor Experience
- Too Expensive
- Missing Features
- Other
- Competitor
- Support Issues

These recorded reasons will be treated as descriptive churn information
rather than automatically interpreted as causal factors.

Further analysis will compare churned and non-churned customers to
identify patterns associated with churn.

---

# 11. Overall Data Quality Assessment

The raw dataset passed the major structural integrity checks.

The main issues requiring treatment are:

1. Missing customer country values
2. Missing support satisfaction scores
3. Business-level duplicate activity records

The missing subscription end dates are considered valid NULL values
because they correspond to active subscriptions.

No orphan customer records, invalid transaction amounts, invalid
transaction statuses, invalid activity values, or subscription logic
violations were identified.

---

# 12. Next Stage

The next stage is:

**Data Cleaning & Transformation**

The cleaning process will create separate cleaned datasets while
preserving the original raw data as the source of truth.

No raw files will be overwritten.
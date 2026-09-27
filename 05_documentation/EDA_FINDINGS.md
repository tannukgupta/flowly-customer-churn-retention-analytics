# Flowly Customer Churn — Preliminary EDA Findings

## Dataset overview

* Total customers: 10,000
* Retained customers: 8,097
* Churned customers: 1,903
* Overall churn rate: 19.03%

This project uses simulated data. Findings describe the generated dataset and should not be presented as real company results.

## Churn by subscription plan

* Free: 23.40%
* Basic: 22.32%
* Business: 16.88%
* Professional: 15.71%

Churn rates vary across plans. This is a descriptive comparison and does not establish that plan choice causes churn.

## Churn reasons

* Low Usage: 322 (16.92%)
* Payment Failure: 296 (15.55%)
* Poor Experience: 270 (14.19%)
* Too Expensive: 261 (13.72%)
* Missing Features: 204 (10.72%)
* Other: 202 (10.61%)
* Competitor: 199 (10.46%)
* Support Issues: 149 (7.83%)

Low Usage was the most frequently recorded churn reason in this dataset.

## Retained versus churned

Retained customers had higher average usage, including sessions, session minutes, projects created, and active days. Churned customers had more support tickets on average. Average satisfaction scores were equal across the two groups.

Churned customers had lower average total revenue and monthly price. Their average failed-transaction count was also lower.

These comparisons may be affected by differences in customer tenure and observation time.

## Payment and support incidence

* Customers with at least one failed payment: 25.87% of retained customers and 16.45% of churned customers.
* Customers with support tickets: 99.05% of retained customers and 99.95% of churned customers.

Ticket presence alone provides little separation between the groups. Further investigation should consider ticket issue types, resolution, volume, and timing.

## Limitations

* Data is simulated, not real customer data.
* Observed relationships are descriptive, not causal.
* Customer tenure and observation windows may affect cumulative metrics such as revenue, sessions, and transactions.
* Recorded churn reasons should be treated as dataset labels, not independently verified causes.
## Stage 7E: Tenure-Normalized Engagement

### Objective

Compare engagement between retained and churned customers while accounting for differences in customer tenure.

### Method

* Parsed signup and churn dates.
* Used the churn date as the analysis end date for churned customers.
* Used 2026-09-18 as the fixed observation cutoff for retained customers.
* Calculated tenure in days.
* Calculated sessions per tenure day and active days per tenure day.
* Checked for missing or non-positive tenure values.

### Data quality

No customers had missing or non-positive tenure values.

### Results

| Metric                             | Retained |  Churned |
| ---------------------------------- | -------: | -------: |
| Customers                          |    8,097 |    1,903 |
| Average tenure (days)              | 379.7791 | 135.1666 |
| Average sessions per tenure day    |   1.0813 |   1.1839 |
| Average active days per tenure day |   0.2124 |   0.2845 |

### Interpretation

Retained customers had substantially longer average tenure. After normalizing cumulative engagement by tenure, churned customers had higher average sessions-per-day and active-days-per-day ratios in this simulated dataset.

This shows why cumulative activity alone can be misleading when comparing groups with different observation durations. The normalized results are descriptive associations, not evidence of causation or proof that these measures predict churn.

### Limitations and next steps

The ratios may still be affected by lifecycle differences, activity timing, and the simulation rules. Further analysis should compare customers over equivalent lifecycle windows, such as the first 30 days after signup, before treating engagement measures as potential churn indicators.
## Stage 7F: First-30-Day Engagement Analysis

### Objective

Compare early customer engagement over a consistent 30-day period to reduce the effect of differences in cumulative customer tenure.

### Method

* Used the signup date as the beginning of each customer's observation window.
* Included activity from the signup date up to, but not including, signup date + 30 days.
* Included customers with recorded tenure of at least 30 days.
* Aggregated sessions, session minutes, projects, files, features used, and active days at the customer level.
* Retained eligible customers with no activity rows in the window and assigned zero to their observed activity totals.

### Eligibility and coverage

* Total customers: 10,000
* Eligible customers with tenure of at least 30 days: 9,868
* Excluded customers with tenure under 30 days: 132
* Activity rows in the first-30-day window: 83,871
* Eligible customers with activity rows in the window: 9,866

Two eligible customers had no activity rows in the first-30-day window. Their activity totals were set to zero for this comparison.

### Results

| Metric                   | Retained |  Churned |
| ------------------------ | -------: | -------: |
| Customers                |    8,097 |    1,771 |
| Average sessions         |  43.3958 |  41.6019 |
| Average session minutes  | 271.9662 | 262.6143 |
| Average projects created |   6.5146 |   6.2309 |
| Average files uploaded   |  26.8017 |  25.5517 |
| Average features used    |  26.5795 |  25.6556 |
| Average active days      |   8.5181 |   8.4133 |

### Interpretation

Retained customers had slightly higher average values across the first-30-day engagement measures than customers who eventually churned. The differences were modest in this descriptive comparison.

Using a consistent early observation window helps reduce the influence of unequal cumulative tenure. However, the analysis does not establish that engagement caused or prevented churn, nor does it demonstrate predictive performance.

### Limitations

* The comparison excludes 132 customers with less than 30 days of recorded tenure.
* Two eligible customers had no activity records in the window; zero activity was assigned for the comparison.
* Results are based on simulated data and reflect its generation rules.
* Further validation would be required before using these measures as operational churn indicators.

### Output files

* `first30_day_customer_engagement.csv`
* `first30_day_engagement_comparison.csv`
## Stage 7G: Support Experience and Churn

### Objective

Explore how support issue types, resolution times, satisfaction scores, and ticket volume relate descriptively to customer churn.

### Data overview

* Support tickets: 31,816
* Unique tickets: 31,816
* Customers with support tickets: 9,922
* Issue types: 6
* Missing satisfaction scores: 20
* Missing customer IDs, ticket dates, issue types, and resolution hours: 0

Missing satisfaction scores were preserved rather than imputed.

### Churn by issue type

| Issue type      | Customers with issue | Churned customers | Churn rate |
| --------------- | -------------------: | ----------------: | ---------: |
| Feature Request |                3,206 |               847 |    26.419% |
| Other           |                3,529 |               929 |    26.325% |
| Billing         |                4,357 |             1,144 |    26.257% |
| Performance     |                4,299 |             1,125 |    26.169% |
| Account         |                3,648 |               925 |    25.356% |
| Technical       |                5,603 |             1,338 |    23.880% |

Customers may appear under multiple issue types, so these groups are not mutually exclusive.

### Support experience by churn status

Average resolution times were generally around 11 hours for both retained and churned customers. Average satisfaction scores were also similar across the issue-type groups, with values generally around 3.4–3.5.

These descriptive averages do not establish that support resolution or satisfaction caused churn.

### Churn by customer ticket volume

| Ticket band | Customers | Churned customers | Churn rate |
| ----------- | --------: | ----------------: | ---------: |
| 1–2 tickets |     3,791 |               212 |     5.592% |
| 3–4 tickets |     4,254 |               625 |    14.692% |
| 5+ tickets  |     1,877 |             1,065 |    56.739% |

The observed churn rate is higher among customers with more support tickets. This association requires further investigation because ticket volume may be affected by tenure, exposure time, and customer lifecycle. It should not be interpreted as evidence that tickets cause churn or as a validated prediction rule.

### Outputs

* `support_issue_churn_summary.csv`
* `support_experience_by_issue_and_churn.csv`
* `support_ticket_volume_churn_summary.csv`

### Limitations and next steps

The analysis uses simulated data. Issue groups overlap, and aggregate ticket counts do not account for when tickets occurred relative to churn. Further analysis should consider comparable observation windows and the timing of support interactions before proposing operational interventions.
## Stage 7H — Payment Failure Label Reconciliation

### Objective

Compare the recorded churn reason against transaction failure history to assess whether the simulated payment data and churn labels align.

### Findings

* There were 1,903 churned customers; 296 (approximately 15.6%) had the churn reason `Payment Failure`.
* Of those 296 customers, 58 had at least one failed transaction recorded, while 238 did not.
* Among the 1,607 churned customers with a different churn reason, 255 had at least one failed transaction recorded.
* The date comparison found a failed transaction on or before the recorded churn date for 57 customers labelled `Payment Failure` and 251 customers with other churn reasons.

### Interpretation and limitations

The churn-reason labels and recorded transaction failures do not align consistently in this simulated dataset. A failed transaction is not exclusive to customers labelled `Payment Failure`, and most customers with that label do not have a failed transaction recorded in the available transaction history.

The date check compares the **latest recorded failed transaction date** with the churn date. It does not check whether any earlier failed transaction occurred before churn when a customer's latest failure was later than churn. Further investigation would be required to determine whether the mismatch reflects simulation rules, the observation window, or the churn-label assignment process.

These are descriptive findings from simulated data. They do not establish that payment failures caused churn.

### Output

* `payment_churn_reason_reconciliation.csv`
## Stage 7H — Part 4: Any Failure Before Churn

### Objective

Improve the payment reconciliation by checking whether each churned customer had **any failed transaction on or before their recorded churn date**, rather than comparing only their latest failed transaction date.

### Findings

* 310 of 1,903 churned customers (16.29%) had at least one failed transaction on or before churn.
* Among 296 customers labelled `Payment Failure`, 58 (19.59%) had a qualifying failed transaction; 238 did not.
* Among 1,607 customers with another churn reason, 252 (15.68%) had a qualifying failed transaction.
* The 310 customers with a qualifying failure had 347 such failed transactions in total.

### Interpretation and limitations

The transaction history and churn-reason labels show incomplete alignment. Some customers labelled `Payment Failure` have no recorded qualifying failed transaction, while customers with other churn reasons do have failures recorded before or on churn.

This is a descriptive reconciliation of the simulated data. It does not establish causation. The analysis depends on the completeness of transaction records and the accuracy of churn dates and labels. Further checks of the simulation's label-generation rules and observation windows may be needed.

### Output files

* `payment_failure_before_churn_customer_check.csv`
* `payment_failure_before_churn_summary.csv`
## Python Final Checks — Dashboard Readiness

### Results

The final customer analytical table contains 10,000 rows and 41 columns, with 10,000 unique customer IDs.

* All required dashboard fields were present.
* No duplicate customer IDs or duplicate full rows were detected.
* No missing or invalid churn values were detected.
* The overall churn rate was 19.03% (1,903 churned customers out of 10,000).
* No infinite values or negative values were detected in the numeric metrics checked.
* Required fields had no missing values.

### Missing-value handling

Missing churn reasons and churn types for retained customers were expected because those fields apply to customers who churned. These values were preserved rather than imputed.

### Output

* `02_python/eda_outputs/final_dashboard_readiness_audit.csv`

### Conclusion

The analytical table passed the structural and selected numeric checks performed by this audit and is ready to proceed to further dashboard preparation. This does not replace business-specific validation of every metric or confirm that all simulated business rules are correct.

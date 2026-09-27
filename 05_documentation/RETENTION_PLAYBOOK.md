# Flowly Customer Churn & Retention Playbook

## 1. Purpose

This playbook translates findings from the Flowly Customer Churn & Retention Analytics project into practical retention actions and measurable experiments.

The dataset is simulated for portfolio and learning purposes. Findings describe patterns in the generated data and should not be interpreted as verified real-world customer behavior or proof of causation.

## 2. Key Findings

### Finding 1 — Overall churn

* Total customers: 10,000
* Churned customers: 1,903
* Retained customers: 8,097
* Overall churn rate: 19.03%

**Interpretation:** Approximately 19% of customers in the simulated dataset are labelled as churned. This provides a baseline for comparing customer groups and evaluating future experiments within the project.

### Finding 2 — Engagement and churn

| Engagement band | Customers | Churned | Churn rate |
| --------------- | --------: | ------: | ---------: |
| Low             |     2,555 |   1,176 |     46.03% |
| Medium-low      |     2,469 |     476 |     19.28% |
| Medium-high     |     2,511 |     211 |      8.40% |
| High            |     2,465 |      40 |      1.62% |

**Interpretation:** Churn rates are higher in the lower-engagement bands in this dataset. This association suggests that engagement could be useful for customer monitoring and further investigation. It does not show that low engagement alone causes churn.

### Finding 3 — Support-ticket volume

| Support-ticket band | Customers | Churned | Churn rate |
| ------------------- | --------: | ------: | ---------: |
| No tickets          |        78 |       1 |      1.28% |
| 1–2                 |     3,791 |     212 |      5.59% |
| 3–4                 |     4,254 |     625 |     14.69% |
| 5+                  |     1,877 |   1,065 |     56.74% |

**Interpretation:** Customers with five or more tickets have a higher observed churn rate than customers in the lower ticket-volume bands. Ticket volume may be a useful signal for investigation, but it may also reflect longer customer tenure, greater product usage, or other factors.

### Finding 4 — Churn by subscription plan

| Plan         | Customers | Churned | Churn rate |
| ------------ | --------: | ------: | ---------: |
| Free         |       893 |     209 |     23.40% |
| Basic        |     3,705 |     827 |     22.32% |
| Business     |     1,588 |     268 |     16.88% |
| Professional |     3,814 |     599 |     15.71% |

**Interpretation:** Churn rates differ across subscription plans in the simulated data. Plan differences should be explored alongside engagement, customer type, tenure, and billing exposure before drawing conclusions about why the rates differ.

### Finding 5 — Churn reason labels

| Recorded churn reason | Customers |
| --------------------- | --------: |
| Low Usage             |       322 |
| Payment Failure       |       296 |
| Poor Experience       |       270 |
| Too Expensive         |       261 |
| Missing Features      |       204 |
| Other                 |       202 |
| Competitor            |       199 |
| Support Issues        |       149 |

**Interpretation:** Low Usage and Payment Failure are the two most frequent recorded churn-reason labels. These labels can help organize follow-up analysis, but they should not be treated as independently verified explanations of churn.

### Finding 6 — Payment patterns require careful interpretation

The proportion of customers with at least one failed transaction is 25.87% among retained customers and 16.45% among churned customers.

**Interpretation:** This pattern does not support a simple conclusion that customers with failed transactions are more likely to churn. The payment-failure churn label should be reconciled with transaction dates, churn dates, and the simulation rules before making payment-related recommendations.

## 3. Evidence limitations

* The dataset is simulated and may not represent a real SaaS customer population.
* Observed associations do not establish causation.
* Customer groups may differ in tenure, usage exposure, plan, or other characteristics.
* Recorded churn reasons are labels in the generated dataset and may reflect programmed rules.
* Recommendations should be tested and evaluated before being treated as effective retention strategies.
## 4. Proposed Retention Actions

### Action 1 — Early engagement support

**Evidence:** The low-engagement band has a churn rate of 46.03%, compared with 1.62% in the high-engagement band.

**Target group:** Newly onboarded customers who show low activity during their first few weeks.

**Proposed intervention:**

* Provide a guided onboarding checklist.
* Introduce customers to key product features through short tutorials.
* Send a helpful check-in when activity falls below a defined threshold.
* Offer access to onboarding support when customers encounter difficulties.

**Hypothesis:** Proactive onboarding may help customers discover product value and increase early engagement.

**KPIs:**

* First-30-day active customer rate
* First-30-day feature adoption rate
* 30-day retention rate
* Onboarding completion rate

**Validation:** Randomly assign eligible new customers to a standard onboarding group and an enhanced onboarding group. Compare outcomes after a predefined observation period.

---

### Action 2 — Support escalation and resolution review

**Evidence:** Customers with five or more support tickets have an observed churn rate of 56.74%, compared with 5.59% for customers with one or two tickets.

**Target group:** Customers with repeated support contacts, especially those with unresolved or recurring issues.

**Proposed intervention:**

* Flag repeated contacts for a support-team review.
* Identify recurring issue categories and investigate common failure points.
* Review whether tickets are being reopened or customers need to repeat information.
* Provide a named point of contact for complex cases where appropriate.

**Hypothesis:** A more coordinated support experience may reduce customer effort and improve satisfaction.

**KPIs:**

* Repeat-contact rate
* First-contact resolution rate
* Average resolution time
* Customer satisfaction after ticket resolution
* Retention rate among eligible customers

**Validation:** Pilot the escalation process with a defined customer group and compare the results with a comparable group receiving the existing support process.

---

### Action 3 — Plan-specific customer research

**Evidence:** Churn rates vary across plans: Free 23.40%, Basic 22.32%, Business 16.88%, and Professional 15.71%.

**Target group:** Customers across subscription plans, analyzed separately rather than assuming one explanation applies to every plan.

**Proposed intervention:**

* Collect feedback about product value, feature needs, and plan fit.
* Review usage and feature adoption by plan.
* Investigate whether customers understand plan limits and available features.
* Consider plan guidance or education where the analysis identifies a clear information gap.

**Hypothesis:** Better understanding of plan-specific needs may help Flowly identify opportunities to improve customer experience.

**KPIs:**

* Churn rate by plan
* Plan-level engagement rate
* Feature adoption by plan
* Customer satisfaction by plan
* Upgrade, downgrade, and cancellation rates, if available

**Validation:** Analyze plan-level outcomes over a consistent period and test any proposed plan guidance or product changes using a controlled pilot where feasible.

---

### Action 4 — Investigate payment-related churn

**Evidence:** Payment Failure is a recorded churn reason for 296 customers. However, the proportion with at least one failed transaction is lower among churned customers than retained customers in the current analysis.

**Target group:** Customers with failed payments, after validating transaction timing and the churn-event records.

**Proposed intervention:**

* Reconcile failed transactions with churn dates.
* Review whether failures were temporary, repeated, or subsequently resolved.
* If supported by the evidence, test payment reminders or clearer payment-recovery instructions.
* Avoid treating every failed transaction as a sign that a customer will churn.

**Hypothesis:** For customers whose payment problems are confirmed to precede cancellation, a timely recovery process may help resolve avoidable payment interruptions.

**KPIs:**

* Payment recovery rate
* Repeat payment-failure rate
* Time to successful payment after a failure
* Churn rate among customers with validated payment issues

**Validation:** First verify the payment and churn data. Then compare a payment-recovery pilot with the existing process, ensuring that customers are eligible based on a clearly defined rule.

---

### Action 5 — Investigate low-usage churn reasons

**Evidence:** Low Usage is the most frequent recorded churn-reason label, with 322 customers.

**Target group:** Customers labelled with Low Usage, and customers whose activity has declined according to a defined monitoring rule.

**Proposed intervention:**

* Review activity trends before the recorded churn date.
* Identify features that customers use less often or fail to adopt.
* Test relevant educational content, onboarding reminders, or product guidance.
* Gather feedback to distinguish lack of awareness from product-fit issues.

**Hypothesis:** Helping customers overcome specific adoption barriers may improve product engagement for some customer groups.

**KPIs:**

* Active customer rate
* Feature adoption rate
* Change in activity after intervention
* 30-day and 60-day retention rates

**Validation:** Define the target population and activity thresholds before running a pilot. Compare engagement and retention outcomes against a suitable comparison group.

---

## 5. Experiment and Measurement Principles

For any retention experiment:

1. Define the eligible customer population before the experiment begins.
2. Specify the intervention and comparison process in advance.
3. Choose a primary KPI and observation window before examining results.
4. Use consistent churn and retention definitions across groups.
5. Compare groups over the same period and account for relevant differences, such as tenure and subscription plan.
6. Report sample sizes and uncertainty where possible.
7. Do not claim that an intervention caused an improvement unless the study design and evidence support that conclusion.
8. Record unsuccessful or inconclusive experiments as well as successful ones.

## 6. Implementation Priority

The actions above are proposed areas for investigation, not a ranking of proven impact. Flowly should first confirm data quality, operational feasibility, customer eligibility, and measurement requirements before selecting a pilot.

## 7. Expected Business Value

If future experiments demonstrate positive results, the retention program could help Flowly:

* Identify customers who may need additional support.
* Improve the onboarding and product-adoption experience.
* Better understand plan-specific customer needs.
* Resolve verified payment problems more effectively.
* Measure retention initiatives using defined business KPIs.

Any realized business value must be measured through subsequent implementation and evaluation. It is not established by the simulated analysis alone.

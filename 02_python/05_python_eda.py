
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "customer_analytical.csv"

OUTPUT_DIR = BASE_DIR / "eda_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Alias for the Stage 7C code
OUTPUT_PATH = OUTPUT_DIR

# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("FLOWLY CUSTOMER CHURN — PYTHON EDA")
print("=" * 70)

print("\n1. DATASET SHAPE")
print("-" * 70)
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]:,}")


# ============================================================
# 3. BASIC STRUCTURE
# ============================================================

print("\n2. COLUMN NAMES")
print("-" * 70)
print(df.columns.tolist())

print("\n3. DATA TYPES")
print("-" * 70)
print(df.dtypes)

print("\n4. FIRST FIVE ROWS")
print("-" * 70)
print(df.head())


# ============================================================
# 4. MISSING VALUES
# ============================================================

print("\n5. MISSING VALUES")
print("-" * 70)

missing = pd.DataFrame({
    "missing_count": df.isna().sum(),
    "missing_percent": (df.isna().mean() * 100).round(2)
})

print(missing[missing["missing_count"] > 0])


# ============================================================
# 5. DUPLICATE CUSTOMER CHECK
# ============================================================

print("\n6. CUSTOMER UNIQUENESS")
print("-" * 70)

print("Total rows:", len(df))
print("Unique customer IDs:", df["customer_id"].nunique())
print("Duplicate customer IDs:", df["customer_id"].duplicated().sum())


# ============================================================
# 6. CHURN DISTRIBUTION
# ============================================================

print("\n7. CHURN DISTRIBUTION")
print("-" * 70)

print(df["churned"].value_counts(dropna=False))

churn_rate = df["churned"].mean() * 100
print(f"\nOverall churn rate: {churn_rate:.2f}%")


# ============================================================
# 7. NUMERICAL SUMMARY
# ============================================================

print("\n8. NUMERICAL SUMMARY")
print("-" * 70)

print(df.describe().T)


# ============================================================
# 8. CHURN VS RETAINED CUSTOMER COMPARISON
# ============================================================

print("\n9. CHURN VS RETAINED CUSTOMER COMPARISON")
print("-" * 70)

comparison_columns = [
    "total_sessions",
    "total_session_minutes",
    "total_projects_created",
    "total_active_days",
    "total_support_tickets",
    "failed_transactions",
    "total_revenue",
    "monthly_price",
    "avg_satisfaction_score"
]

comparison = df.groupby("churned")[comparison_columns].mean().T

comparison.columns = [
    "Retained" if col == 0 else "Churned"
    for col in comparison.columns
]

print(comparison.round(2))


# ============================================================
# 9. CHURN BY PLAN
# ============================================================

print("\n10. CHURN BY PLAN")
print("-" * 70)

plan_analysis = (
    df.groupby("plan")
      .agg(
          customers=("customer_id", "nunique"),
          churned_customers=("churned", "sum"),
          churn_rate=("churned", "mean")
      )
      .reset_index()
)

plan_analysis["churn_rate_percent"] = (
    plan_analysis["churn_rate"] * 100
).round(2)

print(plan_analysis)


# ============================================================
# 10. SAVE TABLE OUTPUTS
# ============================================================

comparison.to_csv(OUTPUT_DIR / "churn_retained_comparison.csv")
plan_analysis.to_csv(OUTPUT_DIR / "churn_by_plan.csv", index=False)

print("\n11. OUTPUT FILES")
print("-" * 70)
print("Saved comparison and plan analysis to:", OUTPUT_DIR)


# ============================================================
# 11. VISUALIZATION — CHURN DISTRIBUTION
# ============================================================

sns.set_theme()

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="churned")

plt.title("Customer Churn Distribution")
plt.xlabel("Churned (0 = Retained, 1 = Churned)")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "churn_distribution.png", dpi=150)
plt.show()


# ============================================================
# 12. VISUALIZATION — CHURN RATE BY PLAN
# ============================================================

plt.figure(figsize=(8, 5))

sns.barplot(
    data=plan_analysis,
    x="plan",
    y="churn_rate_percent"
)

plt.title("Churn Rate by Subscription Plan")
plt.xlabel("Subscription Plan")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "churn_rate_by_plan.png", dpi=150)
plt.show()


print("\n" + "=" * 70)
print("PYTHON EDA — FIRST PASS COMPLETE")
print("=" * 70)


# ============================================================
# STAGE 7C: CHURN REASONS AND RISK SIGNALS
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7C: CHURN REASONS AND RISK SIGNALS")
print("=" * 70)

# 1. Churn reasons
if "churn_reason" in df.columns:
    churn_reasons = (
        df[df["churned"] == 1]
        .groupby("churn_reason")
        .size()
        .reset_index(name="customers")
        .sort_values("customers", ascending=False)
    )

    churn_reasons["share_percent"] = (
        churn_reasons["customers"]
        / churn_reasons["customers"].sum()
        * 100
    ).round(2)

    print("\nCHURN REASONS")
    print(churn_reasons.to_string(index=False))

    churn_reasons.to_csv(
        OUTPUT_PATH / "churn_reasons.csv",
        index=False
    )
else:
    print("\nColumn 'churn_reason' not found. Check your column names.")

# 2. Compare failed-payment incidence
if "failed_transactions" in df.columns:
    payment_comparison = (
        df.assign(
            had_failed_payment=df["failed_transactions"] > 0
        )
        .groupby("churned")
        .agg(
            customers=("churned", "size"),
            customers_with_failed_payment=("had_failed_payment", "sum")
        )
        .reset_index()
    )

    payment_comparison["failed_payment_percent"] = (
        payment_comparison["customers_with_failed_payment"]
        / payment_comparison["customers"]
        * 100
    ).round(2)

    payment_comparison["customer_group"] = (
        payment_comparison["churned"]
        .map({0: "Retained", 1: "Churned"})
    )

    print("\nFAILED PAYMENT INCIDENCE")
    print(payment_comparison.to_string(index=False))

    payment_comparison.to_csv(
        OUTPUT_PATH / "failed_payment_incidence.csv",
        index=False
    )

# 3. Compare support ticket incidence
if "total_support_tickets" in df.columns:
    support_comparison = (
        df.assign(
            had_support_ticket=df["total_support_tickets"] > 0
        )
        .groupby("churned")
        .agg(
            customers=("churned", "size"),
            customers_with_tickets=("had_support_ticket", "sum")
        )
        .reset_index()
    )

    support_comparison["ticket_customer_percent"] = (
        support_comparison["customers_with_tickets"]
        / support_comparison["customers"]
        * 100
    ).round(2)

    support_comparison["customer_group"] = (
        support_comparison["churned"]
        .map({0: "Retained", 1: "Churned"})
    )

    print("\nSUPPORT TICKET INCIDENCE")
    print(support_comparison.to_string(index=False))

    support_comparison.to_csv(
        OUTPUT_PATH / "support_ticket_incidence.csv",
        index=False
    )

print("\nStage 7C analysis complete.")

# ============================================================
# STAGE 7D: SEGMENT-LEVEL INVESTIGATION
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7D: SEGMENT-LEVEL INVESTIGATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. CREATE ENGAGEMENT BANDS
# ------------------------------------------------------------

df["engagement_band"] = pd.qcut(
    df["total_active_days"],
    q=4,
    labels=[
        "Low Engagement",
        "Medium-Low Engagement",
        "Medium-High Engagement",
        "High Engagement"
    ],
    duplicates="drop"
)

engagement_analysis = (
    df.groupby("engagement_band", observed=False)
      .agg(
          customers=("customer_id", "nunique"),
          churned_customers=("churned", "sum"),
          churn_rate=("churned", "mean"),
          avg_sessions=("total_sessions", "mean"),
          avg_projects=("total_projects_created", "mean")
      )
      .reset_index()
)

engagement_analysis["churn_rate_percent"] = (
    engagement_analysis["churn_rate"] * 100
).round(2)

print("\nENGAGEMENT BAND ANALYSIS")
print(engagement_analysis.to_string(index=False))

engagement_analysis.to_csv(
    OUTPUT_DIR / "engagement_band_analysis.csv",
    index=False
)

# ------------------------------------------------------------
# 2. CHURN BY PLAN AND ENGAGEMENT BAND
# ------------------------------------------------------------

plan_engagement_analysis = (
    df.groupby(
        ["plan", "engagement_band"],
        observed=False
    )
    .agg(
        customers=("customer_id", "nunique"),
        churned_customers=("churned", "sum"),
        churn_rate=("churned", "mean")
    )
    .reset_index()
)

plan_engagement_analysis["churn_rate_percent"] = (
    plan_engagement_analysis["churn_rate"] * 100
).round(2)

print("\nCHURN BY PLAN AND ENGAGEMENT BAND")
print(plan_engagement_analysis.to_string(index=False))

plan_engagement_analysis.to_csv(
    OUTPUT_DIR / "plan_engagement_churn.csv",
    index=False
)
# ------------------------------------------------------------
# 3. SUPPORT TICKET VOLUME ANALYSIS
# ------------------------------------------------------------

df["support_band"] = pd.cut(
    df["total_support_tickets"],
    bins=[-1, 0, 2, 4, float("inf")],
    labels=[
        "No Tickets",
        "1-2 Tickets",
        "3-4 Tickets",
        "5+ Tickets"
    ]
)

support_band_analysis = (
    df.groupby("support_band", observed=False)
      .agg(
          customers=("customer_id", "nunique"),
          churned_customers=("churned", "sum"),
          churn_rate=("churned", "mean"),
          avg_resolution_hours=("avg_resolution_hours", "mean"),
          avg_satisfaction_score=("avg_satisfaction_score", "mean")
      )
      .reset_index()
)

support_band_analysis["churn_rate_percent"] = (
    support_band_analysis["churn_rate"] * 100
).round(2)

print("\nSUPPORT VOLUME ANALYSIS")
print(support_band_analysis.to_string(index=False))

support_band_analysis.to_csv(
    OUTPUT_DIR / "support_volume_analysis.csv",
    index=False
)
# ------------------------------------------------------------
# 4. FAILED PAYMENT INCIDENCE BY PLAN
# ------------------------------------------------------------

df["had_failed_payment"] = df["failed_transactions"] > 0

payment_plan_analysis = (
    df.groupby("plan")
      .agg(
          customers=("customer_id", "nunique"),
          customers_with_failed_payment=("had_failed_payment", "sum"),
          churned_customers=("churned", "sum")
      )
      .reset_index()
)

payment_plan_analysis["failed_payment_percent"] = (
    payment_plan_analysis["customers_with_failed_payment"]
    / payment_plan_analysis["customers"]
    * 100
).round(2)

payment_plan_analysis["churn_rate_percent"] = (
    payment_plan_analysis["churned_customers"]
    / payment_plan_analysis["customers"]
    * 100
).round(2)

print("\nFAILED PAYMENT INCIDENCE BY PLAN")
print(payment_plan_analysis.to_string(index=False))

payment_plan_analysis.to_csv(
    OUTPUT_DIR / "payment_by_plan_analysis.csv",
    index=False
)
# ------------------------------------------------------------
# 5. VISUALIZATION — CHURN RATE BY ENGAGEMENT BAND
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

sns.barplot(
    data=engagement_analysis,
    x="engagement_band",
    y="churn_rate_percent"
)

plt.title("Churn Rate by Engagement Band")
plt.xlabel("Engagement Band")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "churn_rate_by_engagement_band.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 6. VISUALIZATION — CHURN RATE BY SUPPORT VOLUME
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    data=support_band_analysis,
    x="support_band",
    y="churn_rate_percent"
)

plt.title("Churn Rate by Support Ticket Volume")
plt.xlabel("Support Ticket Band")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "churn_rate_by_support_volume.png",
    dpi=150
)

plt.show()


print("\nStage 7D analysis complete.")

# ============================================================
# STAGE 7E: TENURE-NORMALIZED ENGAGEMENT
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7E: TENURE-NORMALIZED ENGAGEMENT")
print("=" * 70)

# Parse dates
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["churn_date"] = pd.to_datetime(df["churn_date"], errors="coerce")

# Fixed observation cutoff for reproducibility
observation_cutoff = pd.Timestamp("2026-09-18")

# For churned customers, use churn date.
# For retained customers, use the observation cutoff.
df["analysis_end_date"] = df["churn_date"].fillna(observation_cutoff)

# Calculate customer tenure
df["tenure_days"] = (
    df["analysis_end_date"] - df["signup_date"]
).dt.days

# Check invalid tenure values before calculating rates
invalid_tenure = df["tenure_days"].isna() | (df["tenure_days"] <= 0)

print("\nTENURE QUALITY CHECK")
print("Missing or non-positive tenure:", invalid_tenure.sum())

# Avoid dividing by zero or using invalid tenure
valid_tenure = df["tenure_days"] > 0

df["sessions_per_tenure_day"] = np.where(
    valid_tenure,
    df["total_sessions"] / df["tenure_days"],
    np.nan
)

df["active_days_per_tenure_day"] = np.where(
    valid_tenure,
    df["total_active_days"] / df["tenure_days"],
    np.nan
)

# Compare tenure-normalized engagement by churn status
tenure_comparison = (
    df.groupby("churned")
      .agg(
          customers=("customer_id", "nunique"),
          avg_tenure_days=("tenure_days", "mean"),
          avg_sessions_per_day=("sessions_per_tenure_day", "mean"),
          avg_active_days_per_day=("active_days_per_tenure_day", "mean")
      )
      .reset_index()
)

tenure_comparison["customer_group"] = (
    tenure_comparison["churned"]
    .map({0: "Retained", 1: "Churned"})
)

print("\nTENURE-NORMALIZED ENGAGEMENT COMPARISON")
print(tenure_comparison.round(4).to_string(index=False))

tenure_comparison.to_csv(
    OUTPUT_DIR / "tenure_normalized_engagement.csv",
    index=False
)

print("\nStage 7E tenure analysis complete.")

# ============================================================
# STAGE 7F: FIRST-30-DAY ENGAGEMENT — DATA INSPECTION
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7F: FIRST-30-DAY ENGAGEMENT — DATA INSPECTION")
print("=" * 70)

# Load cleaned customer activity data

activity_path = (
    BASE_DIR.parent
    / "01_raw_data"
    / "cleaned"
    / "customer_activity_cleaned.csv"
)
activity = pd.read_csv(activity_path)

# Parse dates
activity["activity_date"] = pd.to_datetime(
    activity["activity_date"], errors="coerce"
)

# Inspect structure and date range
print("\nACTIVITY DATA SHAPE")
print(activity.shape)

print("\nACTIVITY DATE RANGE")
print("Earliest activity:", activity["activity_date"].min())
print("Latest activity:", activity["activity_date"].max())

print("\nMISSING VALUES")
print(activity[["customer_id", "activity_date"]].isna().sum())

print("\nACTIVITY ROWS PER CUSTOMER — SUMMARY")
activity_rows_per_customer = activity.groupby("customer_id").size()

print(activity_rows_per_customer.describe().round(2))

print("\nCUSTOMER ANALYTICAL DATE COLUMNS")
print(df[["customer_id", "signup_date", "churn_date"]].head(5).to_string(index=False))

print("\nStage 7F inspection complete.")

# ============================================================
# STAGE 7F: FIRST-30-DAY ENGAGEMENT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7F: FIRST-30-DAY ENGAGEMENT ANALYSIS")
print("=" * 70)

# Ensure date columns are in datetime format
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["churn_date"] = pd.to_datetime(df["churn_date"], errors="coerce")
activity["activity_date"] = pd.to_datetime(
    activity["activity_date"], errors="coerce"
)

# Only include customers with at least 30 days of recorded tenure
eligible_customers = df.loc[
    df["tenure_days"] >= 30,
    [
        "customer_id",
        "signup_date",
        "churned",
        "tenure_days"
    ]
].copy()

print("\nCUSTOMER ELIGIBILITY")
print("Total customers:", df["customer_id"].nunique())
print("Eligible customers (tenure >= 30 days):",
      eligible_customers["customer_id"].nunique())
print("Excluded customers (tenure < 30 days):",
      df["customer_id"].nunique()
      - eligible_customers["customer_id"].nunique())

# Attach signup dates to activity records
first30_activity = activity.merge(
    eligible_customers[["customer_id", "signup_date"]],
    on="customer_id",
    how="inner"
)

# Keep activity in the first 30 days after signup:
# signup date inclusive, signup date + 30 days exclusive
first30_activity = first30_activity.loc[
    (first30_activity["activity_date"] >= first30_activity["signup_date"])
    & (
        first30_activity["activity_date"]
        < first30_activity["signup_date"] + pd.Timedelta(days=30)
    )
].copy()

print("\nFIRST-30-DAY ACTIVITY ROWS")
print("Rows within the first 30 days:", len(first30_activity))
print("Customers with activity in the window:",
      first30_activity["customer_id"].nunique())

# Aggregate the activity measures for each customer
activity_metrics = [
    "sessions",
    "session_minutes",
    "projects_created",
    "files_uploaded",
    "features_used",
    "active_days"
]

first30_summary = (
    first30_activity
    .groupby("customer_id")[activity_metrics]
    .sum()
    .reset_index()
)

# Include eligible customers who had no activity rows in the window.
# For these customers, the observed activity total is zero.
first30_customer = eligible_customers.merge(
    first30_summary,
    on="customer_id",
    how="left"
)

first30_customer[activity_metrics] = (
    first30_customer[activity_metrics].fillna(0)
)

# Compare first-30-day activity by eventual churn status
first30_comparison = (
    first30_customer
    .groupby("churned")
    .agg(
        customers=("customer_id", "nunique"),
        avg_sessions=("sessions", "mean"),
        avg_session_minutes=("session_minutes", "mean"),
        avg_projects_created=("projects_created", "mean"),
        avg_files_uploaded=("files_uploaded", "mean"),
        avg_features_used=("features_used", "mean"),
        avg_active_days=("active_days", "mean")
    )
    .reset_index()
)

first30_comparison["customer_group"] = (
    first30_comparison["churned"]
    .map({0: "Retained", 1: "Churned"})
)

print("\nFIRST-30-DAY ENGAGEMENT COMPARISON")
print(first30_comparison.round(4).to_string(index=False))

# Save customer-level first-30-day activity and comparison output
first30_customer.to_csv(
    OUTPUT_DIR / "first30_day_customer_engagement.csv",
    index=False
)

first30_comparison.to_csv(
    OUTPUT_DIR / "first30_day_engagement_comparison.csv",
    index=False
)

print("\nSaved:")
print("- first30_day_customer_engagement.csv")
print("- first30_day_engagement_comparison.csv")

print("\nStage 7F first-30-day analysis complete.")

# ============================================================
# STAGE 7G: SUPPORT EXPERIENCE AND CHURN
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7G: SUPPORT EXPERIENCE AND CHURN")
print("=" * 70)

# Load cleaned support ticket data
support_path = (
    BASE_DIR.parent
    / "01_raw_data"
    / "cleaned"
    / "support_tickets_cleaned.csv"
)

print("\nSupport file path:", support_path)

if not support_path.exists():
    raise FileNotFoundError(
        f"Support file not found: {support_path}"
    )

support = pd.read_csv(support_path)

# Standardize key data types
support["ticket_date"] = pd.to_datetime(
    support["ticket_date"], errors="coerce"
)

support["resolution_hours"] = pd.to_numeric(
    support["resolution_hours"], errors="coerce"
)

support["satisfaction_score"] = pd.to_numeric(
    support["satisfaction_score"], errors="coerce"
)

# Make churn status numeric for reliable grouping
df["churned"] = pd.to_numeric(df["churned"], errors="coerce")

# Attach each customer's churn status to their support tickets
support_analysis = support.merge(
    df[["customer_id", "churned"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print("\nSUPPORT DATA OVERVIEW")
print("Rows:", len(support))
print("Unique tickets:", support["ticket_id"].nunique())
print("Unique customers:", support["customer_id"].nunique())
print("Issue types:", support["issue_type"].nunique())

print("\nMISSING VALUES")
print(
    support[
        [
            "customer_id",
            "ticket_date",
            "issue_type",
            "resolution_hours",
            "satisfaction_score"
        ]
    ].isna().sum()
)

print("\nISSUE TYPE COUNTS")
print(
    support["issue_type"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nSUPPORT STATUS BY CHURN")
print(
    support_analysis.groupby("churned")
    .agg(
        tickets=("ticket_id", "nunique"),
        customers=("customer_id", "nunique"),
        avg_resolution_hours=("resolution_hours", "mean"),
        avg_satisfaction=("satisfaction_score", "mean")
    )
    .round(3)
    .to_string()
)

print("\nStage 7G inspection complete.")

# ============================================================
# STAGE 7G — PART 2: CHURN BY SUPPORT ISSUE TYPE
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7G — PART 2: CHURN BY SUPPORT ISSUE TYPE")
print("=" * 70)

# ------------------------------------------------------------
# 1. Summarize customers and tickets for each issue type
# ------------------------------------------------------------

issue_summary = (
    support_analysis
    .groupby("issue_type")
    .agg(
        customers_with_issue=("customer_id", "nunique"),
        total_tickets=("ticket_id", "nunique"),
        avg_resolution_hours=("resolution_hours", "mean"),
        avg_satisfaction=("satisfaction_score", "mean")
    )
    .reset_index()
)

# Count distinct customers who churned within each issue type
issue_churned = (
    support_analysis[support_analysis["churned"] == 1]
    .groupby("issue_type")["customer_id"]
    .nunique()
    .reset_index(name="churned_customers")
)

issue_summary = issue_summary.merge(
    issue_churned,
    on="issue_type",
    how="left"
)

issue_summary["churned_customers"] = (
    issue_summary["churned_customers"].fillna(0).astype(int)
)

# Churn rate among customers who experienced each issue type
issue_summary["churn_rate_pct"] = (
    issue_summary["churned_customers"]
    / issue_summary["customers_with_issue"]
    * 100
)

issue_summary = issue_summary.sort_values(
    "churn_rate_pct",
    ascending=False
)

print("\nCHURN BY SUPPORT ISSUE TYPE")
print(issue_summary.round(3).to_string(index=False))

# Save issue-level summary
issue_summary.to_csv(
    OUTPUT_DIR / "support_issue_churn_summary.csv",
    index=False
)

# ------------------------------------------------------------
# 2. Compare resolution and satisfaction by issue and churn
# ------------------------------------------------------------

issue_experience = (
    support_analysis
    .groupby(["issue_type", "churned"])
    .agg(
        customers=("customer_id", "nunique"),
        tickets=("ticket_id", "nunique"),
        avg_resolution_hours=("resolution_hours", "mean"),
        avg_satisfaction=("satisfaction_score", "mean")
    )
    .reset_index()
)

issue_experience["customer_group"] = (
    issue_experience["churned"]
    .map({0: "Retained", 1: "Churned"})
)

print("\nSUPPORT EXPERIENCE BY ISSUE TYPE AND CHURN STATUS")
print(issue_experience.round(3).to_string(index=False))

# Save detailed experience summary
issue_experience.to_csv(
    OUTPUT_DIR / "support_experience_by_issue_and_churn.csv",
    index=False
)

# ------------------------------------------------------------
# 3. Customer-level ticket volume and churn
# ------------------------------------------------------------

customer_support = (
    support_analysis
    .groupby(["customer_id", "churned"])
    .agg(
        ticket_count=("ticket_id", "nunique"),
        avg_resolution_hours=("resolution_hours", "mean"),
        avg_satisfaction=("satisfaction_score", "mean")
    )
    .reset_index()
)

# Assign ticket-volume bands
customer_support["ticket_band"] = pd.cut(
    customer_support["ticket_count"],
    bins=[0, 2, 4, float("inf")],
    labels=["1-2 tickets", "3-4 tickets", "5+ tickets"]
)

ticket_band_summary = (
    customer_support
    .groupby("ticket_band", observed=False)
    .agg(
        customers=("customer_id", "nunique"),
        churned_customers=("churned", "sum"),
        avg_tickets=("ticket_count", "mean"),
        avg_resolution_hours=("avg_resolution_hours", "mean"),
        avg_satisfaction=("avg_satisfaction", "mean")
    )
    .reset_index()
)

ticket_band_summary["churn_rate_pct"] = (
    ticket_band_summary["churned_customers"]
    / ticket_band_summary["customers"]
    * 100
)

print("\nCHURN BY CUSTOMER TICKET VOLUME")
print(ticket_band_summary.round(3).to_string(index=False))

ticket_band_summary.to_csv(
    OUTPUT_DIR / "support_ticket_volume_churn_summary.csv",
    index=False
)

print("\nSaved:")
print("- support_issue_churn_summary.csv")
print("- support_experience_by_issue_and_churn.csv")
print("- support_ticket_volume_churn_summary.csv")

print("\nStage 7G Part 2 complete.")

# ============================================================
# STAGE 7H: PAYMENT BEHAVIOUR — DATA INSPECTION
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7H: PAYMENT BEHAVIOUR — DATA INSPECTION")
print("=" * 70)

# Load cleaned transaction data
transaction_path = (
    BASE_DIR.parent
    / "01_raw_data"
    / "cleaned"
    / "transactions_cleaned.csv"
)

print("\nTransaction file path:", transaction_path)

if not transaction_path.exists():
    raise FileNotFoundError(
        f"Transaction file not found: {transaction_path}"
    )

transactions = pd.read_csv(transaction_path)

# Parse and standardize columns
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"], errors="coerce"
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"], errors="coerce"
)

# Attach customer churn status
transaction_analysis = transactions.merge(
    df[["customer_id", "churned"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# ------------------------------------------------------------
# 1. Dataset overview
# ------------------------------------------------------------

print("\nTRANSACTION DATA OVERVIEW")
print("Rows:", len(transactions))
print("Unique transaction IDs:", transactions["transaction_id"].nunique())
print("Unique customers:", transactions["customer_id"].nunique())

print("\nTRANSACTION DATE RANGE")
print("Earliest:", transactions["transaction_date"].min())
print("Latest:", transactions["transaction_date"].max())

print("\nMISSING VALUES")
print(
    transactions[
        [
            "transaction_id",
            "customer_id",
            "transaction_date",
            "amount",
            "payment_method",
            "transaction_status"
        ]
    ].isna().sum()
)

# ------------------------------------------------------------
# 2. Transaction status distribution
# ------------------------------------------------------------

print("\nTRANSACTION STATUS COUNTS")
print(
    transactions["transaction_status"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nTRANSACTION STATUS BY CHURN STATUS")
print(
    transaction_analysis
    .groupby(["churned", "transaction_status"])
    .agg(
        transactions=("transaction_id", "nunique"),
        customers=("customer_id", "nunique"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean")
    )
    .round(3)
    .to_string()
)

# ------------------------------------------------------------
# 3. Payment method distribution
# ------------------------------------------------------------

print("\nPAYMENT METHOD COUNTS")
print(
    transactions["payment_method"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nStage 7H inspection complete.")

# ============================================================
# STAGE 7H — PART 2: CUSTOMER-LEVEL PAYMENT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7H — PART 2: CUSTOMER-LEVEL PAYMENT ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Aggregate transactions for each customer
# ------------------------------------------------------------

customer_payments = (
    transaction_analysis
    .groupby(["customer_id", "churned"])
    .agg(
        total_transactions=("transaction_id", "nunique"),
        successful_transactions=(
            "transaction_status",
            lambda x: (x == "Successful").sum()
        ),
        failed_transactions=(
            "transaction_status",
            lambda x: (x == "Failed").sum()
        ),
        total_transaction_amount=("amount", "sum"),
        avg_transaction_amount=("amount", "mean")
    )
    .reset_index()
)

# Calculate failure rate among recorded transactions
customer_payments["failed_transaction_rate_pct"] = np.where(
    customer_payments["total_transactions"] > 0,
    customer_payments["failed_transactions"]
    / customer_payments["total_transactions"] * 100,
    np.nan
)

customer_payments["has_failed_payment"] = (
    customer_payments["failed_transactions"] > 0
).astype(int)

# ------------------------------------------------------------
# 2. Add customers with no recorded transactions
# ------------------------------------------------------------

all_customers = df[["customer_id", "churned"]].drop_duplicates()

customer_payments = all_customers.merge(
    customer_payments.drop(columns=["churned"]),
    on="customer_id",
    how="left",
    validate="one_to_one"
)

payment_count_columns = [
    "total_transactions",
    "successful_transactions",
    "failed_transactions",
    "total_transaction_amount"
]

customer_payments[payment_count_columns] = (
    customer_payments[payment_count_columns].fillna(0)
)

customer_payments["has_failed_payment"] = (
    customer_payments["has_failed_payment"].fillna(0).astype(int)
)

# Customers without transactions have no observed transaction failure rate.
# Keep their failure rate and average transaction amount missing.
customer_payments["failed_transaction_rate_pct"] = (
    customer_payments["failed_transaction_rate_pct"].where(
        customer_payments["total_transactions"] > 0,
        np.nan
    )
)

# ------------------------------------------------------------
# 3. Compare payment metrics by churn status
# ------------------------------------------------------------

payment_comparison = (
    customer_payments
    .groupby("churned")
    .agg(
        customers=("customer_id", "nunique"),
        customers_with_transactions=(
            "total_transactions",
            lambda x: (x > 0).sum()
        ),
        customers_with_failed_payment=("has_failed_payment", "sum"),
        avg_transactions=("total_transactions", "mean"),
        avg_failed_transactions=("failed_transactions", "mean"),
        avg_failure_rate_pct=("failed_transaction_rate_pct", "mean"),
        avg_transaction_amount=("avg_transaction_amount", "mean"),
        avg_total_transaction_amount=("total_transaction_amount", "mean")
    )
    .reset_index()
)

payment_comparison["customer_group"] = (
    payment_comparison["churned"]
    .map({0: "Retained", 1: "Churned"})
)

payment_comparison["failed_payment_incidence_pct"] = (
    payment_comparison["customers_with_failed_payment"]
    / payment_comparison["customers"]
    * 100
)

payment_comparison["transaction_coverage_pct"] = (
    payment_comparison["customers_with_transactions"]
    / payment_comparison["customers"]
    * 100
)

print("\nCUSTOMER-LEVEL PAYMENT COMPARISON")
print(payment_comparison.round(4).to_string(index=False))

# ------------------------------------------------------------
# 4. Compare payment metrics by plan
# ------------------------------------------------------------

payment_with_plan = customer_payments.merge(
    df[["customer_id", "plan"]],
    on="customer_id",
    how="left",
    validate="one_to_one"
)

plan_payment_summary = (
    payment_with_plan
    .groupby("plan")
    .agg(
        customers=("customer_id", "nunique"),
        customers_with_transactions=(
            "total_transactions",
            lambda x: (x > 0).sum()
        ),
        customers_with_failed_payment=("has_failed_payment", "sum"),
        total_failed_transactions=("failed_transactions", "sum"),
        total_transactions=("total_transactions", "sum")
    )
    .reset_index()
)

plan_payment_summary["failed_payment_incidence_pct"] = (
    plan_payment_summary["customers_with_failed_payment"]
    / plan_payment_summary["customers"]
    * 100
)

plan_payment_summary["transaction_failure_rate_pct"] = np.where(
    plan_payment_summary["total_transactions"] > 0,
    plan_payment_summary["total_failed_transactions"]
    / plan_payment_summary["total_transactions"] * 100,
    np.nan
)

print("\nPAYMENT METRICS BY PLAN")
print(plan_payment_summary.round(4).to_string(index=False))

# ------------------------------------------------------------
# 5. Save results
# ------------------------------------------------------------

customer_payments.to_csv(
    OUTPUT_DIR / "customer_payment_metrics.csv",
    index=False
)

payment_comparison.to_csv(
    OUTPUT_DIR / "payment_comparison_by_churn.csv",
    index=False
)

plan_payment_summary.to_csv(
    OUTPUT_DIR / "payment_metrics_by_plan.csv",
    index=False
)

print("\nSaved:")
print("- customer_payment_metrics.csv")
print("- payment_comparison_by_churn.csv")
print("- payment_metrics_by_plan.csv")

print("\nStage 7H Part 2 complete.")

# ============================================================
# STAGE 7H — PART 3: PAYMENT FAILURE LABEL RECONCILIATION
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7H — PART 3: PAYMENT FAILURE LABEL RECONCILIATION")
print("=" * 70)

# Bring churn reason and churn date onto customer payment records
payment_churn_check = customer_payments.merge(
    df[["customer_id", "churn_reason", "churn_date"]],
    on="customer_id",
    how="left",
    validate="one_to_one"
)

payment_churn_check["churn_date"] = pd.to_datetime(
    payment_churn_check["churn_date"], errors="coerce"
)

# Identify customers whose churn reason is Payment Failure
payment_churn_check["payment_failure_reason"] = (
    payment_churn_check["churn_reason"]
    .eq("Payment Failure")
)

# Identify customers with any failed transaction
payment_churn_check["any_failed_transaction"] = (
    payment_churn_check["failed_transactions"].fillna(0) > 0
)

# Check whether a failed transaction occurred on or before churn date.
# Retained customers have no churn date, so their result remains missing.
customer_failed_dates = (
    transaction_analysis[
        transaction_analysis["transaction_status"] == "Failed"
    ]
    .groupby("customer_id")["transaction_date"]
    .max()
    .reset_index(name="last_failed_transaction_date")
)

payment_churn_check = payment_churn_check.merge(
    customer_failed_dates,
    on="customer_id",
    how="left",
    validate="one_to_one"
)

payment_churn_check["last_failed_transaction_date"] = pd.to_datetime(
    payment_churn_check["last_failed_transaction_date"],
    errors="coerce"
)

payment_churn_check["failed_on_or_before_churn"] = np.where(
    payment_churn_check["churn_date"].notna(),
    (
        payment_churn_check["last_failed_transaction_date"].notna()
        & (
            payment_churn_check["last_failed_transaction_date"]
            <= payment_churn_check["churn_date"]
        )
    ),
    np.nan
)

# ------------------------------------------------------------
# 1. Churn reason counts
# ------------------------------------------------------------

print("\nCHURN REASON COUNTS")
print(
    payment_churn_check.loc[
        payment_churn_check["churned"] == 1,
        "churn_reason"
    ]
    .value_counts(dropna=False)
    .to_string()
)

# ------------------------------------------------------------
# 2. Payment Failure reason versus any failed transaction
# ------------------------------------------------------------

churned_only = payment_churn_check[
    payment_churn_check["churned"] == 1
].copy()

print("\nPAYMENT FAILURE REASON CROSS-CHECK")
print(
    pd.crosstab(
        churned_only["payment_failure_reason"],
        churned_only["any_failed_transaction"],
        margins=True
    ).to_string()
)

# ------------------------------------------------------------
# 3. Failed transaction timing relative to churn
# ------------------------------------------------------------

print("\nFAILED TRANSACTION TIMING AMONG CHURNED CUSTOMERS")
print(
    churned_only.groupby("payment_failure_reason")
    .agg(
        customers=("customer_id", "nunique"),
        customers_with_any_failed_transaction=(
            "any_failed_transaction", "sum"
        ),
        customers_with_failed_transaction_on_or_before_churn=(
            "failed_on_or_before_churn", "sum"
        )
    )
    .to_string()
)

# ------------------------------------------------------------
# 4. Save reconciliation output
# ------------------------------------------------------------

payment_churn_check.to_csv(
    OUTPUT_DIR / "payment_churn_reason_reconciliation.csv",
    index=False
)

print("\nSaved:")
print("- payment_churn_reason_reconciliation.csv")

print("\nStage 7H Part 3 complete.")

# ============================================================
# STAGE 7H — PART 4: ANY FAILURE BEFORE CHURN
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7H — PART 4: ANY FAILURE BEFORE CHURN")
print("=" * 70)

# 1. Prepare churn dates at customer level
customer_churn_dates = df[
    ["customer_id", "churned", "churn_reason", "churn_date"]
].copy()

customer_churn_dates["churn_date"] = pd.to_datetime(
    customer_churn_dates["churn_date"],
    errors="coerce"
)

# 2. Keep only failed transactions and ensure dates are parsed
failed_tx = transaction_analysis.loc[
    transaction_analysis["transaction_status"].eq("Failed"),
    ["customer_id", "transaction_date"]
].copy()

failed_tx["transaction_date"] = pd.to_datetime(
    failed_tx["transaction_date"],
    errors="coerce"
)

# 3. Attach churn dates to each failed transaction
failed_tx = failed_tx.merge(
    customer_churn_dates[
        ["customer_id", "churned", "churn_date"]
    ],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# 4. Keep failures that occurred on or before churn.
# For retained customers, this timing comparison is not applicable.
failed_tx["failure_on_or_before_churn"] = (
    failed_tx["churned"].eq(1)
    & failed_tx["churn_date"].notna()
    & failed_tx["transaction_date"].notna()
    & (
        failed_tx["transaction_date"]
        <= failed_tx["churn_date"]
    )
)

# 5. Count all failures on or before churn for each customer
failures_before_churn = (
    failed_tx.loc[failed_tx["failure_on_or_before_churn"]]
    .groupby("customer_id")
    .agg(
        failed_transactions_on_or_before_churn=(
            "transaction_date", "size"
        ),
        first_failed_transaction_on_or_before_churn=(
            "transaction_date", "min"
        ),
        last_failed_transaction_on_or_before_churn=(
            "transaction_date", "max"
        )
    )
    .reset_index()
)

# 6. Create one row per customer and attach the counts
failure_timing_check = customer_churn_dates.merge(
    failures_before_churn,
    on="customer_id",
    how="left",
    validate="one_to_one"
)

failure_timing_check[
    "failed_transactions_on_or_before_churn"
] = failure_timing_check[
    "failed_transactions_on_or_before_churn"
].fillna(0).astype(int)

failure_timing_check["any_failure_on_or_before_churn"] = (
    failure_timing_check[
        "failed_transactions_on_or_before_churn"
    ] > 0
)

failure_timing_check["payment_failure_reason"] = (
    failure_timing_check["churn_reason"].eq("Payment Failure")
)

# 7. Summarize churned customers by churn reason label
churned_timing = failure_timing_check.loc[
    failure_timing_check["churned"].eq(1)
].copy()

timing_summary = (
    churned_timing.groupby("payment_failure_reason")
    .agg(
        customers=("customer_id", "nunique"),
        customers_with_any_failure_before_churn=(
            "any_failure_on_or_before_churn", "sum"
        ),
        total_failures_before_churn=(
            "failed_transactions_on_or_before_churn", "sum"
        )
    )
    .reset_index()
)

timing_summary["customer_failure_pct"] = (
    timing_summary["customers_with_any_failure_before_churn"]
    / timing_summary["customers"] * 100
).round(2)

print("\nFAILURE TIMING SUMMARY")
print(timing_summary.to_string(index=False))

print("\nCROSS-TAB: CHURN LABEL VS FAILURE BEFORE CHURN")
print(
    pd.crosstab(
        churned_timing["payment_failure_reason"],
        churned_timing["any_failure_on_or_before_churn"],
        margins=True
    ).to_string()
)

# 8. Save customer-level reconciliation and summary
failure_timing_check.to_csv(
    OUTPUT_DIR / "payment_failure_before_churn_customer_check.csv",
    index=False
)

timing_summary.to_csv(
    OUTPUT_DIR / "payment_failure_before_churn_summary.csv",
    index=False
)

print("\nSaved:")
print("- payment_failure_before_churn_customer_check.csv")
print("- payment_failure_before_churn_summary.csv")
print("\nStage 7H Part 4 complete.")
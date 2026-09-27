import pandas as pd
from pathlib import Path

# ==========================================================
# FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS
# STEP 2: DATA QUALITY INVESTIGATION
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "01_raw_data"

print("=" * 80)
print("FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS")
print("STEP 2 - DATA QUALITY INVESTIGATION")
print("=" * 80)


# ----------------------------------------------------------
# Load all tables
# ----------------------------------------------------------

customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
subscriptions = pd.read_csv(RAW_DATA_DIR / "subscriptions.csv")
transactions = pd.read_csv(RAW_DATA_DIR / "transactions.csv")
activity = pd.read_csv(RAW_DATA_DIR / "customer_activity.csv")
support = pd.read_csv(RAW_DATA_DIR / "support_tickets.csv")
marketing = pd.read_csv(RAW_DATA_DIR / "marketing_interactions.csv")
churn = pd.read_csv(RAW_DATA_DIR / "churn_events.csv")


# ==========================================================
# 1. PRIMARY KEY CHECKS
# ==========================================================

print("\n" + "=" * 80)
print("1. PRIMARY KEY CHECKS")
print("=" * 80)

primary_keys = {
    "customers": (customers, "customer_id"),
    "subscriptions": (subscriptions, "subscription_id"),
    "transactions": (transactions, "transaction_id"),
    "customer_activity": (activity, "activity_id"),
    "support_tickets": (support, "ticket_id"),
    "marketing_interactions": (marketing, "interaction_id"),
    "churn_events": (churn, "churn_id")
}

for table_name, (df, key) in primary_keys.items():

    duplicate_keys = df[key].duplicated().sum()

    print(
        f"{table_name:25s} | "
        f"Duplicate {key}: {duplicate_keys:,}"
    )


# ==========================================================
# 2. FOREIGN KEY CHECKS
# ==========================================================

print("\n" + "=" * 80)
print("2. FOREIGN KEY CHECKS")
print("=" * 80)

customer_ids = set(customers["customer_id"])

child_tables = {
    "subscriptions": subscriptions,
    "transactions": transactions,
    "customer_activity": activity,
    "support_tickets": support,
    "marketing_interactions": marketing,
    "churn_events": churn
}

for table_name, df in child_tables.items():

    orphan_count = (
        ~df["customer_id"].isin(customer_ids)
    ).sum()

    print(
        f"{table_name:25s} | "
        f"Orphan customer IDs: {orphan_count:,}"
    )


# ==========================================================
# 3. MISSING VALUE CHECK
# ==========================================================

print("\n" + "=" * 80)
print("3. MISSING VALUE CHECK")
print("=" * 80)

tables = {
    "customers": customers,
    "subscriptions": subscriptions,
    "transactions": transactions,
    "customer_activity": activity,
    "support_tickets": support,
    "marketing_interactions": marketing,
    "churn_events": churn
}

for table_name, df in tables.items():

    print(f"\n{table_name}")

    missing = df.isna().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:
        print("  No missing values.")
    else:
        print(missing)


# ==========================================================
# 4. BUSINESS DUPLICATES IN ACTIVITY
# ==========================================================

print("\n" + "=" * 80)
print("4. BUSINESS DUPLICATES - CUSTOMER ACTIVITY")
print("=" * 80)

activity_business_columns = [
    "customer_id",
    "activity_date",
    "sessions",
    "session_minutes",
    "projects_created",
    "files_uploaded",
    "features_used",
    "active_days"
]

business_duplicate_mask = activity.duplicated(
    subset=activity_business_columns,
    keep=False
)

business_duplicates = activity[
    business_duplicate_mask
]

print(
    f"Rows involved in business duplicates: "
    f"{len(business_duplicates):,}"
)

print(
    f"Duplicate business groups: "
    f"{business_duplicates.groupby(activity_business_columns).ngroups:,}"
)


# ==========================================================
# 5. TRANSACTION VALIDATION
# ==========================================================

print("\n" + "=" * 80)
print("5. TRANSACTION VALIDATION")
print("=" * 80)

negative_transactions = (
    transactions["amount"] < 0
).sum()

print(
    f"Negative transaction amounts: "
    f"{negative_transactions:,}"
)

valid_transaction_statuses = {
    "Successful",
    "Failed",
    "Refunded"
}

invalid_transaction_status = (
    ~transactions["transaction_status"]
    .isin(valid_transaction_statuses)
).sum()

print(
    f"Invalid transaction statuses: "
    f"{invalid_transaction_status:,}"
)


# ==========================================================
# 6. SUPPORT TICKET VALIDATION
# ==========================================================

print("\n" + "=" * 80)
print("6. SUPPORT TICKET VALIDATION")
print("=" * 80)

invalid_satisfaction = (
    support["satisfaction_score"].notna()
    & ~support["satisfaction_score"].between(1, 5)
).sum()

print(
    f"Invalid satisfaction scores: "
    f"{invalid_satisfaction:,}"
)

negative_resolution = (
    support["resolution_hours"] < 0
).sum()

print(
    f"Negative resolution hours: "
    f"{negative_resolution:,}"
)


# ==========================================================
# 7. ACTIVITY VALIDATION
# ==========================================================

print("\n" + "=" * 80)
print("7. CUSTOMER ACTIVITY VALIDATION")
print("=" * 80)

activity_checks = {
    "sessions < 1": (activity["sessions"] < 1).sum(),
    "session_minutes < 0": (
        activity["session_minutes"] < 0
    ).sum(),
    "projects_created < 0": (
        activity["projects_created"] < 0
    ).sum(),
    "files_uploaded < 0": (
        activity["files_uploaded"] < 0
    ).sum(),
    "features_used < 1": (
        activity["features_used"] < 1
    ).sum()
}

for check, count in activity_checks.items():
    print(f"{check:25s}: {count:,}")


# ==========================================================
# 8. SUBSCRIPTION LOGIC
# ==========================================================

print("\n" + "=" * 80)
print("8. SUBSCRIPTION LOGIC CHECK")
print("=" * 80)

# Active subscriptions should not have an end date.
active_with_end_date = (
    (subscriptions["status"] == "Active")
    & subscriptions["end_date"].notna()
).sum()

# Cancelled subscriptions should have an end date.
cancelled_without_end_date = (
    (subscriptions["status"] == "Cancelled")
    & subscriptions["end_date"].isna()
).sum()

print(
    f"Active subscriptions with end date: "
    f"{active_with_end_date:,}"
)

print(
    f"Cancelled subscriptions without end date: "
    f"{cancelled_without_end_date:,}"
)


# ==========================================================
# 9. CHURN VALIDATION
# ==========================================================

print("\n" + "=" * 80)
print("9. CHURN VALIDATION")
print("=" * 80)

churn_customer_duplicates = (
    churn["customer_id"].duplicated().sum()
)

print(
    f"Customers with repeated churn events: "
    f"{churn_customer_duplicates:,}"
)

print("\nChurn types:")
print(churn["churn_type"].value_counts())

print("\nChurn reasons:")
print(churn["churn_reason"].value_counts())


# ==========================================================
# FINAL
# ==========================================================

print("\n" + "=" * 80)
print("DATA QUALITY INVESTIGATION COMPLETED")
print("=" * 80)
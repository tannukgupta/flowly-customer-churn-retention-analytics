from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(
    r"c:\Users\dell\Documents\Data_Analytics_Projects\02_Customer Churn & Retention Analytics"
)

RAW_DATA_DIR = PROJECT_DIR / "01_raw_data"
CLEANED_DATA_DIR = RAW_DATA_DIR / "cleaned"


# ============================================================
# 2. FILES
# ============================================================

FILES = [
    "customers",
    "subscriptions",
    "transactions",
    "customer_activity",
    "support_tickets",
    "marketing_interactions",
    "churn_events"
]


# ============================================================
# 3. LOAD CLEANED DATA
# ============================================================

data = {}

for table in FILES:
    file_path = CLEANED_DATA_DIR / f"{table}_cleaned.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Cleaned file not found: {file_path}"
        )

    data[table] = pd.read_csv(file_path)

print("=" * 70)
print("CLEANED DATA VALIDATION")
print("=" * 70)


# ============================================================
# 4. ROW COUNT COMPARISON
# ============================================================

print("\n1. ROW COUNT COMPARISON")
print("-" * 70)

for table in FILES:

    raw_path = RAW_DATA_DIR / f"{table}.csv"

    raw_df = pd.read_csv(raw_path)
    clean_df = data[table]

    difference = len(raw_df) - len(clean_df)

    print(
        f"{table:25} "
        f"Raw: {len(raw_df):6} | "
        f"Cleaned: {len(clean_df):6} | "
        f"Removed: {difference:4}"
    )


# ============================================================
# 5. MISSING COUNTRY VALIDATION
# ============================================================

print("\n2. CUSTOMER COUNTRY VALIDATION")
print("-" * 70)

customers = data["customers"]

missing_country = customers["country"].isna().sum()

print(f"Missing country values: {missing_country}")

if missing_country == 0:
    print("PASS: All missing country values handled.")
else:
    print("FAIL: Missing country values still exist.")


# ============================================================
# 6. PRIMARY KEY VALIDATION
# ============================================================

print("\n3. PRIMARY KEY VALIDATION")
print("-" * 70)

primary_keys = {
    "customers": "customer_id",
    "subscriptions": "subscription_id",
    "transactions": "transaction_id",
    "customer_activity": "activity_id",
    "support_tickets": "ticket_id",
    "marketing_interactions": "interaction_id",
    "churn_events": "churn_id"
}

for table, key in primary_keys.items():

    df = data[table]

    null_count = df[key].isna().sum()
    duplicate_count = df[key].duplicated().sum()

    print(
        f"{table:25} "
        f"NULL IDs: {null_count:3} | "
        f"Duplicate IDs: {duplicate_count:3}"
    )


# ============================================================
# 7. FOREIGN KEY VALIDATION
# ============================================================

print("\n4. FOREIGN KEY VALIDATION")
print("-" * 70)

customer_ids = set(customers["customer_id"].dropna())

child_tables = [
    "subscriptions",
    "transactions",
    "customer_activity",
    "support_tickets",
    "marketing_interactions",
    "churn_events"
]

for table in child_tables:

    df = data[table]

    orphan_count = (~df["customer_id"].isin(customer_ids)).sum()

    print(
        f"{table:25} "
        f"Orphan customer IDs: {orphan_count}"
    )


# ============================================================
# 8. BUSINESS DUPLICATE VALIDATION
# ============================================================

print("\n5. CUSTOMER ACTIVITY BUSINESS DUPLICATE VALIDATION")
print("-" * 70)

activity = data["customer_activity"]

business_columns = [
    "customer_id",
    "activity_date",
    "sessions",
    "session_minutes",
    "projects_created",
    "files_uploaded",
    "features_used",
    "active_days"
]

duplicate_rows = activity.duplicated(
    subset=business_columns,
    keep=False
).sum()

duplicate_groups = activity.duplicated(
    subset=business_columns,
    keep=False
).sum()

print(f"Business duplicate rows remaining: {duplicate_rows}")

if duplicate_rows == 0:
    print("PASS: Business duplicates removed.")
else:
    print("WARNING: Business duplicates still exist.")


# ============================================================
# 9. TRANSACTION VALIDATION
# ============================================================

print("\n6. TRANSACTION VALIDATION")
print("-" * 70)

transactions = data["transactions"]

negative_amounts = (
    transactions["amount"] < 0
).sum()

valid_statuses = {
    "Successful",
    "Failed"
}

invalid_statuses = (
    ~transactions["transaction_status"].isin(valid_statuses)
).sum()

print(f"Negative transaction amounts: {negative_amounts}")
print(f"Invalid transaction statuses: {invalid_statuses}")


# ============================================================
# 10. ACTIVITY VALIDATION
# ============================================================

print("\n7. CUSTOMER ACTIVITY VALIDATION")
print("-" * 70)

activity_checks = {
    "Sessions < 1": (activity["sessions"] < 1).sum(),
    "Session minutes < 0": (activity["session_minutes"] < 0).sum(),
    "Projects created < 0": (activity["projects_created"] < 0).sum(),
    "Files uploaded < 0": (activity["files_uploaded"] < 0).sum(),
    "Features used < 1": (activity["features_used"] < 1).sum()
}

for check, count in activity_checks.items():
    print(f"{check:25}: {count}")


# ============================================================
# 11. SUPPORT TICKET VALIDATION
# ============================================================

print("\n8. SUPPORT TICKET VALIDATION")
print("-" * 70)

support = data["support_tickets"]

invalid_satisfaction = (
    ~support["satisfaction_score"].dropna().between(1, 5)
).sum()

negative_resolution = (
    support["resolution_hours"] < 0
).sum()

missing_satisfaction = (
    support["satisfaction_score"].isna()
).sum()

print(
    f"Invalid satisfaction scores: {invalid_satisfaction}"
)

print(
    f"Negative resolution hours: {negative_resolution}"
)

print(
    f"Missing satisfaction scores retained: {missing_satisfaction}"
)


# ============================================================
# 12. SUBSCRIPTION LOGIC VALIDATION
# ============================================================

print("\n9. SUBSCRIPTION LOGIC VALIDATION")
print("-" * 70)

subscriptions = data["subscriptions"]

active_with_end_date = (
    (subscriptions["status"] == "Active") &
    (subscriptions["end_date"].notna())
).sum()

cancelled_without_end_date = (
    (subscriptions["status"] == "Cancelled") &
    (subscriptions["end_date"].isna())
).sum()

print(
    f"Active subscriptions with end date: "
    f"{active_with_end_date}"
)

print(
    f"Cancelled subscriptions without end date: "
    f"{cancelled_without_end_date}"
)


# ============================================================
# 13. CHURN VALIDATION
# ============================================================

print("\n10. CHURN VALIDATION")
print("-" * 70)

churn = data["churn_events"]

duplicate_churn_events = (
    churn["customer_id"].duplicated()
).sum()

print(
    f"Repeated customer churn events: "
    f"{duplicate_churn_events}"
)

print("\nChurn type distribution:")

print(
    churn["churn_type"].value_counts()
)


# ============================================================
# 14. DATA TYPE VALIDATION
# ============================================================

print("\n11. IMPORTANT DATA TYPES")
print("-" * 70)

for table in FILES:

    df = data[table]

    print(f"\n{table}")

    print(
        df.dtypes.to_string()
    )


# ============================================================
# 15. FINAL VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

print("""
The cleaned datasets have been checked for:

- Row-count changes
- Missing country values
- Primary key integrity
- Foreign key integrity
- Business duplicates
- Transaction validity
- Activity validity
- Support-ticket validity
- Subscription logic
- Churn-event integrity
- Important data types

Next step:
SQL database design and loading.
""")
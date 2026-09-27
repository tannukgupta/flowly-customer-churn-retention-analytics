import pandas as pd
from pathlib import Path

# ==========================================================
# FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS
# STEP 3: DATA CLEANING & TRANSFORMATION
# ==========================================================

# ----------------------------------------------------------
# 1. PROJECT PATHS
# ----------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_DIR / "01_raw_data"

CLEANED_DATA_DIR = RAW_DATA_DIR / "cleaned"

CLEANED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("=" * 80)
print("FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS")
print("STEP 3 - DATA CLEANING & TRANSFORMATION")
print("=" * 80)


# ----------------------------------------------------------
# 2. LOAD RAW DATA
# ----------------------------------------------------------

print("\nLoading raw datasets...")

customers = pd.read_csv(
    RAW_DATA_DIR / "customers.csv"
)

subscriptions = pd.read_csv(
    RAW_DATA_DIR / "subscriptions.csv"
)

transactions = pd.read_csv(
    RAW_DATA_DIR / "transactions.csv"
)

activity = pd.read_csv(
    RAW_DATA_DIR / "customer_activity.csv"
)

support = pd.read_csv(
    RAW_DATA_DIR / "support_tickets.csv"
)

marketing = pd.read_csv(
    RAW_DATA_DIR / "marketing_interactions.csv"
)

churn = pd.read_csv(
    RAW_DATA_DIR / "churn_events.csv"
)

print("All datasets loaded successfully.")


# ==========================================================
# 3. CUSTOMERS CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("CUSTOMERS CLEANING")
print("=" * 80)

# Check missing country
missing_country_before = customers["country"].isna().sum()

print(
    f"Missing country before cleaning: "
    f"{missing_country_before}"
)

# Replace missing country with Unknown
customers["country"] = customers["country"].fillna(
    "Unknown"
)

# Standardize text fields
customers["country"] = (
    customers["country"]
    .astype(str)
    .str.strip()
)

customers["age_group"] = (
    customers["age_group"]
    .astype(str)
    .str.strip()
)

customers["company_size"] = (
    customers["company_size"]
    .astype(str)
    .str.strip()
)

customers["acquisition_channel"] = (
    customers["acquisition_channel"]
    .astype(str)
    .str.strip()
)

customers["customer_type"] = (
    customers["customer_type"]
    .astype(str)
    .str.strip()
)

# Convert signup date
customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

print(
    f"Missing country after cleaning: "
    f"{customers['country'].isna().sum()}"
)


# ==========================================================
# 4. SUBSCRIPTIONS CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("SUBSCRIPTIONS CLEANING")
print("=" * 80)

# Convert dates
subscriptions["start_date"] = pd.to_datetime(
    subscriptions["start_date"],
    errors="coerce"
)

subscriptions["end_date"] = pd.to_datetime(
    subscriptions["end_date"],
    errors="coerce"
)

# Convert numeric price
subscriptions["monthly_price"] = pd.to_numeric(
    subscriptions["monthly_price"],
    errors="coerce"
)

# Standardize text
for column in [
    "plan",
    "billing_cycle",
    "status"
]:

    subscriptions[column] = (
        subscriptions[column]
        .astype(str)
        .str.strip()
    )

print("Subscription cleaning completed.")

print(
    f"Valid NULL end dates retained: "
    f"{subscriptions['end_date'].isna().sum()}"
)


# ==========================================================
# 5. TRANSACTIONS CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("TRANSACTIONS CLEANING")
print("=" * 80)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"],
    errors="coerce"
)

for column in [
    "payment_method",
    "transaction_status"
]:

    transactions[column] = (
        transactions[column]
        .astype(str)
        .str.strip()
    )

print("Transaction cleaning completed.")


# ==========================================================
# 6. CUSTOMER ACTIVITY CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("CUSTOMER ACTIVITY CLEANING")
print("=" * 80)

activity["activity_date"] = pd.to_datetime(
    activity["activity_date"],
    errors="coerce"
)

numeric_activity_columns = [
    "sessions",
    "session_minutes",
    "projects_created",
    "files_uploaded",
    "features_used",
    "active_days"
]

for column in numeric_activity_columns:

    activity[column] = pd.to_numeric(
        activity[column],
        errors="coerce"
    )

# Business duplicate definition
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

before_duplicates = len(activity)

activity = activity.drop_duplicates(
    subset=activity_business_columns,
    keep="first"
)

after_duplicates = len(activity)

removed_duplicates = (
    before_duplicates - after_duplicates
)

print(
    f"Business duplicate rows removed: "
    f"{removed_duplicates}"
)


# ==========================================================
# 7. SUPPORT TICKETS CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("SUPPORT TICKETS CLEANING")
print("=" * 80)

support["ticket_date"] = pd.to_datetime(
    support["ticket_date"],
    errors="coerce"
)

support["resolution_hours"] = pd.to_numeric(
    support["resolution_hours"],
    errors="coerce"
)

support["satisfaction_score"] = pd.to_numeric(
    support["satisfaction_score"],
    errors="coerce"
)

for column in [
    "issue_type",
    "resolved"
]:

    support[column] = (
        support[column]
        .astype(str)
        .str.strip()
    )

print(
    f"Missing satisfaction scores retained: "
    f"{support['satisfaction_score'].isna().sum()}"
)


# ==========================================================
# 8. MARKETING INTERACTIONS CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("MARKETING INTERACTIONS CLEANING")
print("=" * 80)

marketing["interaction_date"] = pd.to_datetime(
    marketing["interaction_date"],
    errors="coerce"
)

for column in [
    "channel",
    "interaction_type"
]:

    marketing[column] = (
        marketing[column]
        .astype(str)
        .str.strip()
    )

print("Marketing data cleaning completed.")


# ==========================================================
# 9. CHURN CLEANING
# ==========================================================

print("\n" + "=" * 80)
print("CHURN EVENTS CLEANING")
print("=" * 80)

churn["churn_date"] = pd.to_datetime(
    churn["churn_date"],
    errors="coerce"
)

for column in [
    "churn_reason",
    "churn_type"
]:

    churn[column] = (
        churn[column]
        .astype(str)
        .str.strip()
    )

print("Churn data cleaning completed.")


# ==========================================================
# 10. SAVE CLEANED DATA
# ==========================================================

print("\n" + "=" * 80)
print("SAVING CLEANED DATA")
print("=" * 80)

datasets = {
    "customers": customers,
    "subscriptions": subscriptions,
    "transactions": transactions,
    "customer_activity": activity,
    "support_tickets": support,
    "marketing_interactions": marketing,
    "churn_events": churn
}

for name, dataframe in datasets.items():

    output_path = (
        CLEANED_DATA_DIR
        / f"{name}_cleaned.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved: {output_path.name}"
    )


# ==========================================================
# 11. FINAL SUMMARY
# ==========================================================

print("\n" + "=" * 80)
print("CLEANING SUMMARY")
print("=" * 80)

for name, dataframe in datasets.items():

    print(
        f"{name:25s} : "
        f"{len(dataframe):,} rows"
    )

print("\nDATA CLEANING COMPLETED.")
print(
    f"Cleaned files saved to: "
    f"{CLEANED_DATA_DIR}"
)
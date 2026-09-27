
from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================
# PYTHON FINAL CHECKS — PART 1: DASHBOARD READINESS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "customer_analytical.csv"
OUTPUT_DIR = BASE_DIR / "eda_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 70)
print("PYTHON FINAL CHECKS — DASHBOARD READINESS")
print("=" * 70)

# 1. Load analytical customer table
df_final = pd.read_csv(DATA_PATH)

print("\n1. DATASET STRUCTURE")
print(f"Rows: {df_final.shape[0]:,}")
print(f"Columns: {df_final.shape[1]:,}")
print(f"Unique customer IDs: {df_final['customer_id'].nunique():,}")

# 2. Required fields
required_columns = [
    "customer_id",
    "churned",
    "plan",
    "total_revenue",
    "monthly_price",
    "total_sessions",
    "total_active_days",
    "total_support_tickets",
    "failed_transactions"
]

missing_columns = [
    col for col in required_columns
    if col not in df_final.columns
]

print("\n2. REQUIRED COLUMN CHECK")
if missing_columns:
    print("Missing required columns:", missing_columns)
else:
    print("All required columns are present.")

# 3. Customer-level uniqueness
duplicate_customer_ids = df_final["customer_id"].duplicated().sum()

print("\n3. CUSTOMER UNIQUENESS")
print(f"Duplicate customer_id rows: {duplicate_customer_ids}")

# 4. Churn values and churn rate
print("\n4. CHURN VALIDATION")
print("Churn value counts:")
print(df_final["churned"].value_counts(dropna=False).to_string())

valid_churn_values = df_final["churned"].isin([0, 1])
invalid_churn_rows = (~valid_churn_values).sum()

print(f"Invalid or missing churn values: {invalid_churn_rows}")

if valid_churn_values.all():
    churn_rate = df_final["churned"].mean() * 100
    print(f"Overall churn rate: {churn_rate:.2f}%")
else:
    print("Churn rate not calculated because invalid values exist.")

# 5. Missing values in required fields
print("\n5. MISSING VALUES IN REQUIRED FIELDS")
for col in required_columns:
    if col in df_final.columns:
        missing_count = df_final[col].isna().sum()
        print(f"{col}: {missing_count:,}")

# 6. Duplicate full rows
full_row_duplicates = df_final.duplicated().sum()

print("\n6. FULL-ROW DUPLICATES")
print(f"Duplicate full rows: {full_row_duplicates}")

# 7. Numeric anomalies
numeric_columns = df_final.select_dtypes(
    include=["number"]
).columns.tolist()

print("\n7. NUMERIC ANOMALY CHECKS")

infinite_counts = {}
for col in numeric_columns:
    values = df_final[col]
    if values.notna().any():
        infinite_counts[col] = np.isinf(values).sum()

columns_with_infinity = {
    col: count for col, count in infinite_counts.items()
    if count > 0
}

print("Columns containing infinite values:")
print(columns_with_infinity if columns_with_infinity else "None")

nonnegative_metrics = [
    "total_revenue",
    "monthly_price",
    "total_sessions",
    "total_session_minutes",
    "total_projects_created",
    "total_files_uploaded",
    "total_active_days",
    "total_support_tickets",
    "failed_transactions",
    "successful_transactions"
]

for col in nonnegative_metrics:
    if col in df_final.columns:
        negative_count = (df_final[col] < 0).sum()
        print(f"{col} — negative values: {negative_count:,}")

# 8. Category checks
print("\n8. CATEGORY CHECKS")

for col in ["plan", "churn_reason", "churn_type"]:
    if col in df_final.columns:
        print(f"\n{col} value counts:")
        print(df_final[col].value_counts(dropna=False).to_string())

# 9. Save final audit summary
audit_summary = pd.DataFrame({
    "check": [
        "row_count",
        "column_count",
        "unique_customer_ids",
        "duplicate_customer_id_rows",
        "duplicate_full_rows",
        "invalid_or_missing_churn_values",
        "missing_required_columns"
    ],
    "result": [
        len(df_final),
        df_final.shape[1],
        df_final["customer_id"].nunique(),
        int(duplicate_customer_ids),
        int(full_row_duplicates),
        int(invalid_churn_rows),
        ", ".join(missing_columns) if missing_columns else "None"
    ]
})

audit_summary.to_csv(
    OUTPUT_DIR / "final_dashboard_readiness_audit.csv",
    index=False
)

print("\nSaved:")
print("- final_dashboard_readiness_audit.csv")
print("\nDashboard-readiness audit complete.")

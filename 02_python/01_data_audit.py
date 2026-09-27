import pandas as pd
from pathlib import Path

# ==========================================================
# FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS
# STEP 1: RAW DATA AUDIT
# ==========================================================

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "01_raw_data"

# Raw files
FILES = [
    "customers.csv",
    "subscriptions.csv",
    "transactions.csv",
    "customer_activity.csv",
    "support_tickets.csv",
    "marketing_interactions.csv",
    "churn_events.csv"
]

print("=" * 80)
print("FLOWLY CUSTOMER CHURN & RETENTION ANALYTICS")
print("STEP 1 - RAW DATA AUDIT")
print("=" * 80)

for file_name in FILES:

    print("\n")
    print("#" * 80)
    print(f"FILE: {file_name}")
    print("#" * 80)

    file_path = RAW_DATA_DIR / file_name

    # Check file exists
    if not file_path.exists():
        print(f"ERROR: File not found -> {file_path}")
        continue

    # Read CSV
    df = pd.read_csv(file_path)

    # ------------------------------------------------------
    # 1. Shape
    # ------------------------------------------------------
    print("\n1. DATASET SHAPE")
    print("-" * 40)
    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]:,}")

    # ------------------------------------------------------
    # 2. Column names
    # ------------------------------------------------------
    print("\n2. COLUMN NAMES")
    print("-" * 40)

    for column in df.columns:
        print(column)

    # ------------------------------------------------------
    # 3. Data types
    # ------------------------------------------------------
    print("\n3. DATA TYPES")
    print("-" * 40)
    print(df.dtypes)

    # ------------------------------------------------------
    # 4. Missing values
    # ------------------------------------------------------
    print("\n4. MISSING VALUES")
    print("-" * 40)

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values found.")
    else:
        print(missing)

    # ------------------------------------------------------
    # 5. Missing percentage
    # ------------------------------------------------------
    print("\n5. MISSING VALUE PERCENTAGE")
    print("-" * 40)

    missing_pct = (df.isnull().mean() * 100).round(2)

    missing_pct = missing_pct[missing_pct > 0]

    if len(missing_pct) == 0:
        print("No missing values found.")
    else:
        print(missing_pct)

    # ------------------------------------------------------
    # 6. Exact duplicate rows
    # ------------------------------------------------------
    print("\n6. EXACT DUPLICATE ROWS")
    print("-" * 40)

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows: {duplicate_count:,}")

    # ------------------------------------------------------
    # 7. Unique values
    # ------------------------------------------------------
    print("\n7. UNIQUE VALUES")
    print("-" * 40)

    print(df.nunique())

    # ------------------------------------------------------
    # 8. First five records
    # ------------------------------------------------------
    print("\n8. SAMPLE RECORDS")
    print("-" * 40)

    print(df.head())

    # ------------------------------------------------------
    # 9. Numeric statistics
    # ------------------------------------------------------
    print("\n9. NUMERIC SUMMARY")
    print("-" * 40)

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) == 0:
        print("No numeric columns.")
    else:
        print(df[numeric_columns].describe().round(2))

    # ------------------------------------------------------
    # 10. Basic categorical inspection
    # ------------------------------------------------------
    print("\n10. CATEGORICAL VALUE COUNTS")
    print("-" * 40)

    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in categorical_columns:

        # Avoid dumping huge ID columns
        if "id" in column.lower():
            continue

        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False).head(15))


print("\n")
print("=" * 80)
print("RAW DATA AUDIT COMPLETED")
print("=" * 80)
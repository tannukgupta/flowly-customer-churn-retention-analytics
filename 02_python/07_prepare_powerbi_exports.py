
from pathlib import Path
import pandas as pd

# ============================================================
# POWER BI PREPARATION — EXPORTS AND DATA DICTIONARY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

SOURCE_PATH = BASE_DIR / "customer_analytical.csv"
EXPORT_DIR = PROJECT_DIR / "04_powerbi" / "data"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 70)
print("POWER BI PREPARATION — EXPORTS AND DATA DICTIONARY")
print("=" * 70)

# 1. Load analytical dataset
df = pd.read_csv(SOURCE_PATH)

print("\n1. SOURCE DATA")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")
print(f"Unique customers: {df['customer_id'].nunique():,}")

# 2. Basic customer-grain check
duplicate_ids = df["customer_id"].duplicated().sum()

print("\n2. CUSTOMER GRAIN CHECK")
print(f"Duplicate customer IDs: {duplicate_ids}")

if duplicate_ids > 0:
    raise ValueError(
        "Duplicate customer IDs detected. Resolve these before exporting."
    )

# 3. Identify date-like columns and standardize date formatting
date_columns = [
    col for col in df.columns
    if "date" in col.lower()
]

print("\n3. DATE COLUMNS")
print(date_columns if date_columns else "No date-named columns detected.")

for col in date_columns:
    parsed_dates = pd.to_datetime(df[col], errors="coerce")
    df[col] = parsed_dates.dt.strftime("%Y-%m-%d")
    df[col] = df[col].where(parsed_dates.notna(), None)

# 4. Export Power BI-ready CSV
powerbi_csv_path = EXPORT_DIR / "customer_analytical_powerbi.csv"
df.to_csv(powerbi_csv_path, index=False)

print("\n4. POWER BI CSV")
print(f"Saved: {powerbi_csv_path}")

# 5. Create data dictionary
dictionary_rows = []

for col in df.columns:
    dictionary_rows.append({
        "column_name": col,
        "pandas_data_type": str(df[col].dtype),
        "missing_values": int(df[col].isna().sum()),
        "distinct_values": int(df[col].nunique(dropna=True)),
        "sample_values": " | ".join(
            df[col].dropna().astype(str).unique()[:5]
        )
    })

data_dictionary = pd.DataFrame(dictionary_rows)

dictionary_path = EXPORT_DIR / "customer_analytical_data_dictionary.csv"
data_dictionary.to_csv(dictionary_path, index=False)

print("\n5. DATA DICTIONARY")
print(f"Columns documented: {len(data_dictionary):,}")
print(f"Saved: {dictionary_path}")

# 6. Export summary
summary = pd.DataFrame({
    "metric": [
        "row_count",
        "column_count",
        "unique_customer_ids",
        "duplicate_customer_ids",
        "date_column_count"
    ],
    "value": [
        len(df),
        len(df.columns),
        df["customer_id"].nunique(),
        int(duplicate_ids),
        len(date_columns)
    ]
})

summary_path = EXPORT_DIR / "powerbi_export_summary.csv"
summary.to_csv(summary_path, index=False)

print("\n6. EXPORT SUMMARY")
print(summary.to_string(index=False))

print("\nCreated files:")
print("- customer_analytical_powerbi.csv")
print("- customer_analytical_data_dictionary.csv")
print("- powerbi_export_summary.csv")

print("\nPower BI export preparation complete.")
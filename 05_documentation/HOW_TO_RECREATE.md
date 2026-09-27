# How to Recreate the Flowly Raw Data

## Option 1 — Run locally

1. Install Python 3.10+.
2. Put `generate_flowly_data.py` in an empty folder.
3. Open Command Prompt / PowerShell in that folder.
4. Run:

```bash
python generate_flowly_data.py
```

5. A folder named `flowly_churn_project` will be created with the CSV files.

## Option 2 — Run in Google Colab

1. Open a new Python notebook.
2. Upload `generate_flowly_data.py`.
3. Run:

```python
!python generate_flowly_data.py
```

4. Download the generated `flowly_churn_project` folder as a ZIP.

## What to show a recruiter

The strongest proof is the combination of:

- the Python generation code;
- `DATA_PROVENANCE.md`;
- `generation_manifest.json`;
- the raw CSVs;
- later, your SQL scripts and Power BI file.

Do not describe the simulated data as real company data.

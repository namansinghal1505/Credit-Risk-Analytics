"""
Credit Risk Analytics - Data Quality Checks

Runs the data-management checks that should happen before any analysis or modelling:
completeness, uniqueness, validity, consistency and class balance.
Prints a pass/flag report and saves it to outputs/data_quality_report.csv.
"""
from pathlib import Path

import pandas as pd
from utils import load_data

df = load_data()
checks = []


def record(name, passed, detail):
    checks.append({"check": name, "status": "PASS" if passed else "FLAG", "detail": detail})


# Completeness
record("No missing values", df.isna().sum().sum() == 0, f"{df.isna().sum().sum()} nulls")

# Uniqueness
record("Customer_ID unique", df["Customer_ID"].is_unique, f"{df['Customer_ID'].duplicated().sum()} duplicates")
record("Loan_ID unique", df["Loan_ID"].is_unique, f"{df['Loan_ID'].duplicated().sum()} duplicates")
record("No fully duplicated rows", not df.duplicated().any(), f"{df.duplicated().sum()} duplicate rows")

# Validity (ranges)
record("Credit score within 300-900", df["Credit_Score"].between(300, 900).all(),
       f"min={df['Credit_Score'].min()}, max={df['Credit_Score'].max()}")
record("Age within 18-100", df["Age"].between(18, 100).all(), f"min={df['Age'].min()}, max={df['Age'].max()}")
record("Interest rate between 0 and 30", df["Interest_Rate"].between(0, 30).all(),
       f"min={df['Interest_Rate'].min()}, max={df['Interest_Rate'].max()}")

# Consistency
bad_dates = (df["Approval_Date"] < df["Application_Date"]).sum()
record("Approval date not before application date", bad_dates == 0, f"{bad_dates} rows")
mismatch = ((df["Loan_Status"] == "Default") != (df["Default_Risk_Flag"] == 1)).sum()
record("Loan_Status consistent with Default_Risk_Flag", mismatch == 0, f"{mismatch} mismatches")

# Definition check: is the 'Debt_to_Income_Ratio_%' column really debt-to-income?
recomputed = df["Loan_Amount"] / df["Annual_Income"] * 100
max_diff = (recomputed - df["Debt_to_Income_Ratio_%"]).abs().max()
record("'Debt_to_Income_Ratio_%' is a true DTI", max_diff > 0.01,
       f"Equals Loan_Amount / Annual_Income x 100 (max diff {max_diff:.3f}). "
       "It is a loan-to-income ratio, not DTI. No existing-debt service data is present.")
record("Loan-to-income ratio within plausible range (<= 100%)",
       (df["Loan_to_Income_Pct"] <= 100).mean() > 0.95,
       f"{(df['Loan_to_Income_Pct'] > 100).mean():.1%} of loans exceed 100% of annual income")

# Class balance
default_rate = df["Default_Risk_Flag"].mean()
record("Target class balance usable for modelling", 0.02 <= default_rate <= 0.98,
       f"Default rate {default_rate:.2%}; only {int((df['Default_Risk_Flag'] == 0).sum())} non-default loans")

report = pd.DataFrame(checks)
pd.set_option("display.max_colwidth", 120, "display.width", 200)
print(report.to_string(index=False))

Path(__file__).resolve().parents[1].joinpath("outputs").mkdir(exist_ok=True)
report.to_csv(Path(__file__).resolve().parents[1] / "outputs" / "data_quality_report.csv", index=False)

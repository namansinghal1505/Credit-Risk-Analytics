"""
Shared helpers for the Credit Risk Analytics project.

load_data()      -> raw dataset with parsed dates
build_features() -> adds engineered risk features used by the model and monitoring scripts
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "Banking_Credit_Risk_Dataset.csv"


def load_data(path=DATA_PATH):
    """Load the credit risk dataset and parse the date columns."""
    df = pd.read_csv(path, parse_dates=["Application_Date", "Approval_Date"])
    # Column name contains '%', which is awkward in SQL/code: keep the original and add a clean alias.
    df["Loan_to_Income_Pct"] = df["Debt_to_Income_Ratio_%"]
    return df


def build_features(df):
    """Feature engineering for risk modelling and monitoring."""
    out = df.copy()

    # Affordability: monthly instalment proxy (simple amortisation, no interest) vs monthly income
    out["Monthly_Income"] = out["Annual_Income"] / 12
    out["Instalment_Proxy"] = out["Loan_Amount"] / out["Loan_Term_Months"]
    out["Instalment_to_Income"] = out["Instalment_Proxy"] / out["Monthly_Income"]

    # Interest-weighted exposure
    out["Annual_Interest_Cost"] = out["Loan_Amount"] * out["Interest_Rate"] / 100
    out["Interest_to_Income"] = out["Annual_Interest_Cost"] / out["Annual_Income"]

    # Liquidity and leverage
    out["Balance_to_Loan"] = out["Account_Balance"] / out["Loan_Amount"]
    out["Loans_per_Dependent"] = out["Existing_Loans_Count"] / (out["Dependents"] + 1)

    # Process feature
    out["Approval_Lag_Days"] = (out["Approval_Date"] - out["Application_Date"]).dt.days
    out["Application_Year"] = out["Application_Date"].dt.year

    # Bands for reporting
    out["Credit_Band"] = pd.cut(
        out["Credit_Score"],
        bins=[299, 499, 649, 749, 900],
        labels=["Poor (300-499)", "Fair (500-649)", "Good (650-749)", "Excellent (750-900)"],
    )
    out["Income_Band"] = pd.qcut(out["Annual_Income"], 4, labels=["Q1 Low", "Q2", "Q3", "Q4 High"])
    return out


NUMERIC_MODEL_FEATURES = [
    "Age", "Annual_Income", "Credit_Score", "Existing_Loans_Count", "Dependents",
    "Account_Balance", "Loan_Amount", "Loan_Term_Months", "Interest_Rate",
    "Loan_to_Income_Pct", "Instalment_to_Income", "Interest_to_Income",
    "Balance_to_Loan", "Loans_per_Dependent",
]
CATEGORICAL_MODEL_FEATURES = ["Gender", "Marital_Status", "Education_Level",
                              "Employment_Type", "Region", "Loan_Purpose"]

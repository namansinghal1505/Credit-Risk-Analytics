"""
Credit Risk Analytics - Model Monitoring (Population Stability Index)

Compares the distribution of key risk features in each application year against a baseline
period (2018-2019) to detect population drift, the standard first check in model monitoring.

PSI rule of thumb: < 0.10 stable | 0.10-0.25 moderate shift (investigate) | > 0.25 significant shift
"""
from pathlib import Path

import numpy as np
import pandas as pd

from utils import build_features, load_data

FEATURES = ["Credit_Score", "Annual_Income", "Loan_Amount", "Interest_Rate", "Loan_to_Income_Pct"]
BASELINE_YEARS = [2018, 2019]
BINS = 10


def psi(expected, actual, bins=BINS):
    """PSI using decile bin edges taken from the baseline (expected) sample."""
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-4, None), np.clip(a, 1e-4, None)  # avoid log(0)
    return float(np.sum((a - e) * np.log(a / e)))


def status(v):
    return "Stable" if v < 0.10 else ("Investigate" if v < 0.25 else "Significant shift")


df = build_features(load_data())
base = df[df["Application_Year"].isin(BASELINE_YEARS)]
years = sorted(y for y in df["Application_Year"].unique() if y not in BASELINE_YEARS)

rows = []
for year in years:
    cur = df[df["Application_Year"] == year]
    for f in FEATURES:
        v = psi(base[f].values, cur[f].values)
        rows.append({"year": year, "feature": f, "psi": round(v, 4), "status": status(v)})

report = pd.DataFrame(rows)
print(f"Baseline: {BASELINE_YEARS} (n={len(base):,})\n")
print(report.pivot(index="feature", columns="year", values="psi").to_string())
print("\nFlags:", report["status"].value_counts().to_dict())

# Outcome monitoring: default rate and average score by year
trend = df.groupby("Application_Year").agg(
    loans=("Loan_ID", "count"),
    default_rate=("Default_Risk_Flag", "mean"),
    avg_credit_score=("Credit_Score", "mean"),
).round(4)
print("\nPortfolio trend\n")
print(trend.to_string())

out_dir = Path(__file__).resolve().parents[1] / "outputs"
out_dir.mkdir(exist_ok=True)
report.to_csv(out_dir / "psi_report.csv", index=False)
trend.to_csv(out_dir / "portfolio_trend.csv")

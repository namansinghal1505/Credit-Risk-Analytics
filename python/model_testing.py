"""
Credit Risk Analytics - Model Testing & Performance Analysis

Tests whether the engineered features can separate non-default (Approved) from
Default loans, using stratified cross-validation and standard credit-risk metrics:
ROC-AUC, Gini and KS statistic.

IMPORTANT LIMITATION: only ~0.4% of loans are non-default (46 of 12,000), so metrics on the
minority class are noisy. Treat results as a demonstration of the validation method on this
dataset, not as a production-ready model.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.stats import ks_2samp

from utils import (CATEGORICAL_MODEL_FEATURES, NUMERIC_MODEL_FEATURES,
                   build_features, load_data)

RANDOM_STATE = 42
df = build_features(load_data())
X = df[NUMERIC_MODEL_FEATURES + CATEGORICAL_MODEL_FEATURES]
y = df["Default_Risk_Flag"]  # 1 = default

pre = ColumnTransformer([
    ("num", StandardScaler(), NUMERIC_MODEL_FEATURES),
    ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_MODEL_FEATURES),
])

models = {
    "Logistic Regression (balanced)": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
rows, fitted = [], {}

for name, clf in models.items():
    pipe = Pipeline([("pre", pre), ("clf", clf)])
    # Out-of-fold predicted probability of default for every loan
    p_default = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1]

    auc = roc_auc_score(y, p_default)
    ks = ks_2samp(p_default[y == 1], p_default[y == 0]).statistic

    rows.append({
        "model": name,
        "roc_auc": round(auc, 3),
        "gini": round(2 * auc - 1, 3),
        "ks": round(ks, 3),
    })
    fitted[name] = Pipeline([("pre", pre), ("clf", clf)]).fit(X, y)

results = pd.DataFrame(rows)
print("5-fold stratified cross-validation (out-of-fold predictions)\n")
print(results.to_string(index=False))

# Which features matter? Standardised logistic coefficients (interpretable for stakeholders)
lr = fitted["Logistic Regression (balanced)"]
names = lr.named_steps["pre"].get_feature_names_out()
coefs = pd.Series(lr.named_steps["clf"].coef_[0], index=names).sort_values(key=abs, ascending=False)
print("\nTop drivers (logistic regression, standardised; positive = higher default risk)\n")
print(coefs.head(8).round(3).to_string())

out_dir = Path(__file__).resolve().parents[1] / "outputs"
out_dir.mkdir(exist_ok=True)
results.to_csv(out_dir / "model_performance.csv", index=False)
coefs.head(15).rename("coefficient").to_csv(out_dir / "top_risk_drivers.csv")

# ---------------------------------------------------------------------------------------------
# Sanity check: is the near-perfect score real signal, or is the label a simple rule?
# ---------------------------------------------------------------------------------------------
approved = df[df["Default_Risk_Flag"] == 0]
rule = (df["Credit_Score"] >= approved["Credit_Score"].min()) & \
       (df["Loan_to_Income_Pct"] <= approved["Loan_to_Income_Pct"].max())
print("\nRule check: Credit_Score >= %d AND loan-to-income <= %.1f%%"
      % (approved["Credit_Score"].min(), approved["Loan_to_Income_Pct"].max()))
print("  Loans matching rule: %d | share of those that are Approved: %.0f%%"
      % (rule.sum(), (df.loc[rule, "Default_Risk_Flag"] == 0).mean() * 100))
print("  Approved loans captured by the rule: %d of %d" % ((rule & (df['Default_Risk_Flag'] == 0)).sum(), len(approved)))
print("  -> The target behaves like a hard-coded eligibility rule, so high AUC reflects the rule,")
print("     not learned behavioural risk. Validate on real performance data before any real use.")

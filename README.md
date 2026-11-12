# Credit Risk Analytics

End-to-end credit risk analysis of a 12,000-loan banking portfolio: data quality validation, SQL analytics,
feature engineering, model testing, model monitoring and a Power BI dashboard for stakeholders.

> **Dataset note:** the data appears synthetic (99.6% of loans are marked Default, 46 are Approved).
> The project demonstrates the analytical workflow and the checks that catch this, not real-world default behaviour.

## What this project covers

| Area | What was done | Where |
|---|---|---|
| Data management | Completeness, uniqueness, validity and consistency checks; found a mislabeled field and a degenerate target | `python/data_quality_checks.py`, `sql/04_data_quality_checks.sql` |
| SQL analytics | Portfolio KPIs, regional concentration, risk segmentation, year-on-year trend using CTEs and window functions | `sql/` |
| Feature engineering | Instalment-to-income, interest-to-income, balance-to-loan, approval lag, credit and income bands | `python/utils.py` |
| Model testing | Logistic regression and gradient boosting, 5-fold stratified CV, AUC / Gini / KS, interpretable drivers | `python/model_testing.py` |
| Model monitoring | Population Stability Index by year versus a 2018-19 baseline, plus outcome trend | `python/model_monitoring_psi.py`, `sql/05_monitoring_trend.sql` |
| Visualisation | 4-page Power BI dashboard; Python pair plot, violin, heatmap, network graph | `powerbi/`, `python/`, `screenshots/` |
| Stakeholder reporting | Plain-language summary of findings and recommendations | `docs/stakeholder_summary.md` |

## Key findings

- **The "Debt_to_Income_Ratio_%" column is not a debt-to-income ratio.** It equals `Loan_Amount / Annual_Income x 100` for every row, so it is a loan-to-income ratio. 95.7% of loans exceed 100% of annual income.
- **The target is almost constant.** 11,954 of 12,000 loans are Default. A model can score very high without learning real risk.
- **Models reach AUC 0.99+ because the label follows a simple rule.** All 46 Approved loans have a credit score of 601 or more and a loan-to-income ratio of 49.7% or less, and no Default loan meets both. This is a data-generation artefact, not behavioural signal.
- **No population drift.** All 20 feature-year PSI values are below 0.02 (threshold for investigation: 0.10).
- **Approved borrowers differ clearly from defaulted ones:** average credit score about 739 versus about 595, and average loan-to-income about 39% versus about 1,076%.
- **Regional default rates are close** (99.45% to 99.75%), so there is no meaningful regional concentration in this data.

## Dashboard structure (Power BI + DAX)

1. Executive Credit Risk Overview: loans issued, portfolio value, default rate, average credit score, loan status distribution
2. Regional Risk and Portfolio Dynamics: regional growth, default rate by region, risk heatmap, income vs exposure
3. Advanced Credit Risk Intelligence: correlation matrix, loan-to-income impact, risk categories
4. Statistical and Relationship Analysis (Python): pair plot, violin plot, correlation heatmap, network graph

## How to run

```bash
pip install -r requirements.txt
cd python
python data_quality_checks.py
python model_testing.py
python model_monitoring_psi.py
```

Outputs are written to `outputs/`. The SQL files use a `credit_risk` table (the raw CSV) and a `v_credit_risk` staging view.
They were tested in DuckDB and use standard syntax that ports to MySQL 8 and Snowflake; only the quoting of the `%` column name differs
(see comments in `sql/00_staging_view.sql`).

## Tools

Python (pandas, scikit-learn, seaborn, matplotlib, NetworkX) | SQL | Power BI | DAX

## Limitations and next steps

- Replace the synthetic data with real repayment history to build and validate a meaningful default model.
- Rebuild a true debt-to-income field (monthly debt payments / monthly income) once existing-debt data is available.
- Add score-band stability (CSI) and back-testing once a production score exists.

-- Data quality checks (SQL version of python/data_quality_checks.py). Each row = one check.
SELECT 'null_credit_score' AS check_name, COUNT(*) AS failing_rows FROM v_credit_risk WHERE Credit_Score IS NULL
UNION ALL
SELECT 'duplicate_loan_id', COUNT(*) - COUNT(DISTINCT Loan_ID) FROM v_credit_risk
UNION ALL
SELECT 'credit_score_out_of_range', COUNT(*) FROM v_credit_risk WHERE Credit_Score NOT BETWEEN 300 AND 900
UNION ALL
SELECT 'approval_before_application', COUNT(*) FROM v_credit_risk WHERE approval_date < application_date
UNION ALL
SELECT 'status_flag_mismatch', COUNT(*) FROM v_credit_risk
    WHERE (Loan_Status = 'Default' AND Default_Risk_Flag <> 1) OR (Loan_Status <> 'Default' AND Default_Risk_Flag <> 0)
UNION ALL
-- Definition check: 'Debt_to_Income_Ratio_%' should NOT equal loan amount / income if it were a true DTI
SELECT 'dti_column_equals_loan_to_income', COUNT(*) FROM v_credit_risk
    WHERE ABS(loan_to_income_pct - Loan_Amount * 100.0 / Annual_Income) < 0.01
UNION ALL
SELECT 'loan_exceeds_annual_income', COUNT(*) FROM v_credit_risk WHERE Loan_Amount > Annual_Income;

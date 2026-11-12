-- Executive KPIs (mirrors Power BI page 1)
SELECT
    COUNT(*)                                          AS total_loans,
    SUM(Loan_Amount)                                  AS portfolio_value,
    ROUND(AVG(Default_Risk_Flag) * 100, 2)            AS default_rate_pct,
    ROUND(AVG(Credit_Score), 1)                       AS avg_credit_score,
    ROUND(AVG(Interest_Rate), 2)                      AS avg_interest_rate_pct,
    ROUND(SUM(CASE WHEN Default_Risk_Flag = 1 THEN Loan_Amount ELSE 0 END) * 100.0
          / SUM(Loan_Amount), 2)                      AS exposure_at_default_pct
FROM v_credit_risk;

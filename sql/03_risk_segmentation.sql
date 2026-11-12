-- Segment risk by credit band and loan purpose
SELECT
    credit_band,
    Loan_Purpose,
    COUNT(*)                                          AS loans,
    SUM(Loan_Amount)                                  AS exposure,
    ROUND(AVG(Default_Risk_Flag) * 100, 2)            AS default_rate_pct,
    ROUND(AVG(loan_to_income_pct), 1)                 AS avg_loan_to_income_pct
FROM v_credit_risk
GROUP BY credit_band, Loan_Purpose
ORDER BY credit_band, default_rate_pct DESC;

-- Regional risk and concentration (mirrors Power BI page 2)
WITH regional AS (
    SELECT
        Region,
        COUNT(*)                                      AS loans,
        SUM(Loan_Amount)                              AS exposure,
        AVG(Default_Risk_Flag)                        AS default_rate,
        AVG(Credit_Score)                             AS avg_score,
        AVG(loan_to_income_pct)                       AS avg_loan_to_income_pct
    FROM v_credit_risk
    GROUP BY Region
)
SELECT
    Region,
    loans,
    exposure,
    ROUND(exposure * 100.0 / SUM(exposure) OVER (), 2)     AS exposure_share_pct,
    ROUND(default_rate * 100, 2)                           AS default_rate_pct,
    ROUND(avg_score, 1)                                    AS avg_credit_score,
    ROUND(avg_loan_to_income_pct, 1)                       AS avg_loan_to_income_pct,
    RANK() OVER (ORDER BY default_rate DESC)               AS risk_rank
FROM regional
ORDER BY risk_rank;

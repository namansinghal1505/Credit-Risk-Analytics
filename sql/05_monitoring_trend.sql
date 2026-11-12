-- Year-on-year monitoring with window functions (SQL counterpart of the PSI/trend report)
WITH yearly AS (
    SELECT
        application_year,
        COUNT(*)                         AS loans,
        AVG(Default_Risk_Flag)           AS default_rate,
        AVG(Credit_Score)                AS avg_score,
        AVG(loan_to_income_pct)          AS avg_loan_to_income_pct
    FROM v_credit_risk
    GROUP BY application_year
)
SELECT
    application_year,
    loans,
    ROUND(default_rate * 100, 3)                                               AS default_rate_pct,
    ROUND((default_rate - LAG(default_rate) OVER (ORDER BY application_year)) * 100, 3) AS default_rate_change_pp,
    ROUND(avg_score, 1)                                                        AS avg_credit_score,
    ROUND(avg_score - LAG(avg_score) OVER (ORDER BY application_year), 1)      AS score_change,
    ROUND(avg_loan_to_income_pct, 1)                                           AS avg_loan_to_income_pct
FROM yearly
ORDER BY application_year;

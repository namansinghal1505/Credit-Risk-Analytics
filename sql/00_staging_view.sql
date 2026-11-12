-- Staging view: clean column names, typed dates, derived fields.
-- Table assumed: credit_risk (raw CSV loaded as-is). Works on MySQL 8+, Snowflake, DuckDB with minor syntax notes below.
--   MySQL:     quote the % column with backticks:   `Debt_to_Income_Ratio_%`
--   Snowflake: quote with double quotes:            "Debt_to_Income_Ratio_%"
CREATE OR REPLACE VIEW v_credit_risk AS
SELECT
    Customer_ID,
    Loan_ID,
    Region,
    Loan_Purpose,
    Employment_Type,
    Credit_Score,
    Annual_Income,
    Loan_Amount,
    Loan_Term_Months,
    Interest_Rate,
    "Debt_to_Income_Ratio_%"                         AS loan_to_income_pct,   -- column is Loan_Amount / Annual_Income * 100
    Loan_Status,
    Default_Risk_Flag,
    CAST(Application_Date AS DATE)                   AS application_date,
    CAST(Approval_Date AS DATE)                      AS approval_date,
    EXTRACT(YEAR FROM CAST(Application_Date AS DATE)) AS application_year,
    CASE
        WHEN Credit_Score < 500 THEN '1 Poor (300-499)'
        WHEN Credit_Score < 650 THEN '2 Fair (500-649)'
        WHEN Credit_Score < 750 THEN '3 Good (650-749)'
        ELSE                         '4 Excellent (750-900)'
    END                                              AS credit_band
FROM credit_risk;

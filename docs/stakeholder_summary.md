# Credit Risk Portfolio Review: Summary for Stakeholders

**Scope:** 12,000 loans applied for between January 2018 and June 2023, total value about 9.38 billion.

## The headline
The portfolio data cannot yet support reliable risk decisions. Two issues need fixing before any model or dashboard figure is used
for decision-making.

## What we found
1. **One field is mislabeled.** The column called "Debt-to-Income" actually measures loan size against annual income. It does not include
   the borrower's existing debt payments. Any report that quotes it as DTI is misleading.
2. **The outcome data is almost one-sided.** 99.6% of loans are recorded as defaults, which is not credible for a real bank portfolio. This points
   to a data extraction or labelling problem, or to test data.
3. **Approvals follow a simple rule.** Every approved loan has a credit score of 601 or more and a loan-to-income ratio under 50%. Models score
   near-perfectly because they find this rule, not because they predict real borrower behaviour.
4. **The population is stable.** Income, credit score, loan size and interest rate show no meaningful change from 2018 to 2023 (all PSI values below 0.02).
5. **Risk does not concentrate by region.** Default rates are within 0.3 percentage points across all five regions.

## What we recommend
| Action | Why | Owner |
|---|---|---|
| Confirm how "default" is defined and sourced | The 99.6% default rate is not credible | Data owner / Risk |
| Rebuild a true DTI field with existing debt payments | Needed for affordability and CDD decisions | Data engineering |
| Obtain real repayment performance data | Required to build and validate a default model | Risk analytics |
| Keep PSI monitoring on credit score and loan-to-income | Early warning of population change | Analytics |

## How to read the numbers
- **PSI (Population Stability Index):** measures whether today's borrowers look like the baseline group. Below 0.10 is stable.
- **AUC / Gini / KS:** measures how well a model separates good from bad loans. Values this high on real data would be a warning sign, not a success.

"""
Credit Risk Analytics Dashboard
Visualization: Financial Correlation Heatmap



Description:
This script generates a correlation heatmap to analyze the
relationships between key financial variables in the banking
credit risk dataset. It helps identify positive or negative
correlations between variables such as income, loan amount,
credit score, interest rate, and debt-to-income ratio.
"""

# Import required libraries
import seaborn as sns
import matplotlib.pyplot as plt

from utils import load_data

# Load the dataset (previously assumed to exist as `dataset`)
dataset = load_data()

# Calculate correlation matrix from the dataset
corr = dataset.select_dtypes('number').drop(columns=['Loan_to_Income_Pct']).corr()

# Create the heatmap visualization
sns.heatmap(
    corr,
    annot=True,        # Shows correlation values inside cells
    cmap="coolwarm"    # Color scheme for positive/negative correlation
)

# Add chart title
plt.title("Financial Variable Correlation Matrix")

# Display the heatmap
plt.show()
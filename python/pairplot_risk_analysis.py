"""
Credit Risk Analytics Dashboard
Visualization: Pair Plot Risk Analysis


Description:
This script generates a pair plot to visualize relationships
between multiple numerical variables in the credit risk dataset.
The pair plot helps identify patterns, correlations, and clusters
between variables such as income, loan amount, credit score,
and debt-to-income ratio.

The data points are colored by Loan_Status to distinguish
between approved and defaulted loans.
"""

# Import required libraries
import seaborn as sns
import matplotlib.pyplot as plt

from utils import load_data

# Load the dataset (previously assumed to exist as `dataset`)
dataset = load_data()

# Generate pair plot for multivariable relationship analysis
cols = ["Annual_Income", "Loan_Amount", "Credit_Score", "Interest_Rate", "Loan_Status"]
sns.pairplot(
    dataset[cols],
    hue="Loan_Status",   # Color the plots based on loan status
    corner=True          # Show only lower triangle to reduce redundancy
)

# Add title to the visualization
plt.suptitle("Multi-Variable Risk Relationship Analysis", y=1.02)

# Display the plot
plt.show()
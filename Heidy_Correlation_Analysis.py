#
# Heidy, 2025/10/22
# File: Heidy_Correltion_Analysis.py
# Apply correlation analysis to business problems
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats

# 1. Input
df = pd.read_csv('Correlation_Analysis_Data.csv')

df.info()
print(df.iloc[:,1:6])

# correlation, pvalue = stats.pearsonr(df['Marketing_Spend'],
#                                      df['Sales_Revenue'],)

# 2. Process
correlation_matrix = df.iloc[:,1:6].corr()

print(correlation_matrix.round(3))

# print(df.isnull().sum())
# print(df.isnull().sum().sum())

# 3. Output
# print('Data loaded successfully!')
# print(f'Dataset shape: {df.shape}')
# print(f"Correlation: {correlation:.2f}")
# print(f"P value: {pvalue:.4e}")
sns.heatmap(correlation_matrix)
plt.title('Heidy is the most intelligent person in the world')
plt.tight_layout()
plt.show()
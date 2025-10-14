#
# Heidy, 2025/10/08
# File: Heidy_Excel.py
# Calculate sum of column in Excel file.
#

import os
import pandas as pd


# Read file result
result_df = pd.read_excel('Financial_Sample_with_total.xlsx')
# Remove spaces in column names
result_df.columns = result_df.columns.str.strip()

# Read original file
original_df = pd.read_excel('Financial_Sample.xlsx')
original_df.columns = original_df.columns.str.strip()

# Show last 5 rows
print(result_df.tail())

# Verify
print("Expected Sales total:", original_df['Sales'].sum())
print("Saved file Sales total:", result_df['Sales'].iloc[-1])
    

#
# Heidy, 2025/10/19
# File: VanessaHeidy_Project1.py
# Project 1: Sales Performance Analyzer
#

import pandas as pd

# 1. Input
data = pd.read_excel("Sales_Data.xlsx")

total_bonus = 0
print("SALES PERFORMANCE REPORT")
print("========================")

# 2. Process
# Loop
for index, row in data.iterrows():
    name = row['Employee_Name']
    sales = row['Monthly_Sales']
    target = row['Sales_Target']
    
    if sales >= target:
        status = "Target MET"
        bonus = sales * 0.10
    else:
        status = "Target NOT MET"
        bonus = sales * 0.05
    
    total_bonus += bonus

    print(f"{name}: {status} | Sales: ${sales:,.0f} | Bonus: ${bonus:,.0f}")

# 3. Output
print(f"\nTotal Bonuses to Pay: ${total_bonus:,.0f}")
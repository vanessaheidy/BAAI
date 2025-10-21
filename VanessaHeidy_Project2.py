#
# Heidy, 2025/10/21
# File: VanessaHeidy_Project2.py
# Project 2: Inventory Reorder System
#

import pandas as pd

# 1. Input
data = pd.read_excel("Inventory.xlsx")

total_cost = 0
good_stock = []

print("INVENTORY REORDER REPORT")
print("========================")
print("Products Needing Reorder:")

# 2. Process
# Loop
for index, row in data.iterrows():
    product = row['Product_Name']
    current = row['Current_Stock']
    minimum = row['Minimum_Stock']
    price = row['Unit_Price']
    
    if current < minimum:
        reorder_qty = (minimum - current) + 10  # Safety buffer
        cost = reorder_qty * price
        total_cost += cost
        print(f"{product}: Reorder {reorder_qty} units | Cost: ${cost:,.0f}")
    else:
        good_stock.append(product)

# 3. Output
print(f"\nTotal Reorder Cost: ${total_cost:,.0f}")
print("Products in Good Stock: " + ", ".join(good_stock))
#
# Heidy, 2025/10/19
# File: VanessaHeidy_Project3.py
# Project 3: Customer Segmentation Tool
#

import pandas as pd

# 1. Input
data = pd.read_excel("Customers.xlsx")

vip_customers = []
regular_customers = []
new_customers = []
vip_revenue = 0

print("CUSTOMER SEGMENTATION REPORT")
print("============================")

# 2. Process
# Loop
for index, row in data.iterrows():
    name = row['Customer_Name']
    total = row['Total_Purchases']
    orders = row['Number_of_Orders']
    avg_order = total / orders

    if total > 10000:
        vip_customers.append((name, total, orders, avg_order))
        vip_revenue += total
    elif total >= 5000:
        regular_customers.append((name, total, orders, avg_order))
    else:
        new_customers.append((name, total, orders, avg_order))

# 3. Output
print("VIP Customers:")
for cust in vip_customers:
    print(f"- {cust[0]} | Total: ${cust[1]:,.2f} | Orders: {cust[2]} | Avg Order: ${cust[3]:,.2f}")

print("\nRegular Customers:")
for cust in regular_customers:
    print(f"- {cust[0]} | Total: ${cust[1]:,.2f} | Orders: {cust[2]} | Avg Order: ${cust[3]:,.2f}")

print("\nNew Customers:")
for cust in new_customers:
    print(f"- {cust[0]} | Total: ${cust[1]:,.2f} | Orders: {cust[2]} | Avg Order: ${cust[3]:,.2f}")

print(f"\nTotal VIP Revenue: ${vip_revenue:,.0f}")
#
# Heidy, 2025/09/24
# File: VanessaHeidy_MiniProject.py
# Mini Project: Discount Calculator 
#

# 1. Input
# Data Provided
products = [
    {"name": "Laptop", "price": 1200, "category": "Electronics"},
    {"name": "Shirt", "price": 45, "category": "Clothing"},
    {"name": "Phone", "price": 800, "category": "Electronics"},
    {"name": "Shoes", "price": 120, "category": "Clothing"},
    {"name": "Tablet", "price": 350, "category": "Electronics"},
    {"name": "Jacket", "price": 95, "category": "Clothing"},
    {"name": "Book", "price": 25, "category": "Books"},
    {"name": "Headphones", "price": 150, "category": "Electronics"}
]
# Initialize tracking variabel
total_original = 0
total_discount_amount = 0
total_final = 0

# Bonus tracking variable
highest_discount_product = None
highest_discount_value = 0
total_discount_percentage = 0

category_count = {}
most_expensive_after_discount = None
cheapest_after_discount = None

print("---PRODUCT DISCOUNT CALCULATOR---\n")

# 2. Process
# Loop
for product in products:
    name = product["name"]
    price = product["price"]
    category = product["category"]
    # Determine discound base on category and price
    total_discount_percentage = 0
    if category == "Electronics":
        if price >= 1000:
            discount_percetage = 20
        elif price >= 500:
            discount_percetage = 15
        else:
            discount_percetage = 10
    elif category == "Clothing":
        if price >= 100:
            discount_percetage = 25
        else: 
            discount_percetage = 15
    elif category == "Books":
        discount_percetage = 10

    # Calculate final price
    discount_amount = price * (discount_percetage / 100)
    final_price = price - discount_amount

    # Clearance
    clearance_tag = ""
    if discount_percetage >= 20:
        clearance_tag = "[Clearance]"

    # Updates total
    total_original += price
    total_discount_amount += discount_amount
    total_final += final_price
    total_discount_percentage += discount_percetage

    # Highest discount product
    if discount_amount > highest_discount_value:
        highest_discount_value = discount_amount
        highest_discount_product = name

    # Product per category
    category_count[category] = category_count.get(category, 0) + 1

    # The most expensive and the cheapest
    if most_expensive_after_discount is None or final_price > most_expensive_after_discount["final_price"]:
        most_expensive_after_discount = {"name": name, "final_price": final_price}
    if cheapest_after_discount is None or final_price < cheapest_after_discount["final_price"]:
        cheapest_after_discount = {"name": name, "final_price": final_price}

    # 3. Output
    # Print product detail
    print(f"Product: {name} {clearance_tag}")
    print(f"Category: {category}")
    print(f"Original Price: ${price:.2f}")
    print(f"Discount: {discount_percetage}%")
    print(f"Final Price: ${final_price:.2f}\n")

# Summary
print("---SUMMARY---")
print(f"Total Products: {len(products)}")
print(f"Total Original Price: ${total_original:.2f}")
print(f"Total Discount: ${total_discount_amount:.2f}")
print(f"Total Final Price: ${total_final:.2f}")

# Bonus Level 1
average_discount_percentage = total_discount_percentage / len(products)
print("\n---BONUS LEVEL 1---")
print(f"Product with highest discount amount: {highest_discount_product} (${highest_discount_value:.2f})")
print(f"Average discount percentage: {average_discount_percentage:.2f}%")

# Bonus Level 2
print("\n---BONUS LEVEL 2---")
print("Product count per category:")
for cat, count in category_count.items():
    print(f"{cat}: {count}")
print(f"Most expensive after discount: {most_expensive_after_discount['name']} (${most_expensive_after_discount['final_price']:.2f})")
print(f"Cheapest after discount: {cheapest_after_discount['name']} (${cheapest_after_discount['final_price']:.2f})")

# Bonus Level 3
print("\n---BONUS LEVEL 3---")
print(f"Total savings for customer: ${total_discount_amount:.2f}")
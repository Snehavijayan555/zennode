# Catalog
catalog = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount Rules
discount_rules = {
    "flat_10_discount": {"condition": lambda cart_total: cart_total > 200, "discount_amount": 10},
    "bulk_5_discount": {"condition": lambda quantity: quantity > 10, "discount_percentage": 0.05},
    "bulk_10_discount": {"condition": lambda quantity: quantity > 20, "discount_percentage": 0.1},
    "tiered_50_discount": {"condition": lambda quantity, product_quantity: quantity > 30 and product_quantity > 15,
                           "discount_percentage": 0.5}
}

# Fees
gift_wrap_fee_per_unit = 1
shipping_fee_per_package = 5
units_per_package = 10


def apply_discount_rules(cart_total, quantities):
    applicable_discounts = {}
    
    # Check if flat_10_discount is applicable
    if discount_rules["flat_10_discount"]["condition"](cart_total):
        applicable_discounts["flat_10_discount"] = discount_rules["flat_10_discount"]["discount_amount"]
    
    # Check if bulk_5_discount or bulk_10_discount is applicable
    for product, quantity in quantities.items():
        if discount_rules["bulk_5_discount"]["condition"](quantity):
            applicable_discounts["bulk_5_discount"] = discount_rules["bulk_5_discount"]["discount_percentage"]
            break
        elif discount_rules["bulk_10_discount"]["condition"](quantity):
            applicable_discounts["bulk_10_discount"] = discount_rules["bulk_10_discount"]["discount_percentage"]
            break
    
    # Check if tiered_50_discount is applicable
    for product, quantity in quantities.items():
        if discount_rules["tiered_50_discount"]["condition"](cart_total, quantity):
            applicable_discounts["tiered_50_discount"] = discount_rules["tiered_50_discount"]["discount_percentage"]
            break
    
    return applicable_discounts


def calculate_total_amount(quantities, discounts):
    total_amount = 0
    
    for product, quantity in quantities.items():
        if product in catalog:
            price = catalog[product]
            if product in discounts:
                discount = discounts[product]
                discounted_price = price - (price * discount)
                total_amount += quantity * discounted_price
            else:
                total_amount += quantity * price
    
    return total_amount


def calculate_shipping_fee(units):
    return (units - 1) // units_per_package * shipping_fee_per_package


def calculate_gift_wrap_fee(quantities):
    total_units = sum(quantities.values())
    return total_units * gift_wrap_fee_per_unit


# User input
quantities = {}
is_gift_wrapped = {}

for product in catalog:
    quantity = int(input(f"Enter the quantity of {product}: "))
    quantities[product] = quantity
    
    gift_wrapped = input(f"Is {product} wrapped as a gift? (yes/no): ")
    is_gift_wrapped[product] = gift_wrapped.lower() == "yes"

# Calculate subtotal
subtotal = calculate_total_amount(quantities, {})

# Apply discount rules
applicable_discounts = apply_discount_rules(subtotal, quantities)

# Calculate total amount after discount
total_amount = calculate_total_amount(quantities, applicable_discounts)

# Calculate shipping fee
shipping_fee = calculate_shipping_fee(sum(quantities.values()))

# Calculate gift wrap fee
gift_wrap_fee = calculate_gift_wrap_fee(quantities)

# Display output
print("\n--- Order Summary ---")
for product, quantity in quantities.items():
    total_product_amount = catalog[product] * quantity
    print(f"{product}: {quantity} x ${catalog[product]} = ${total_product_amount}")

print(f"\nSubtotal: ${subtotal}")

if applicable_discounts:
    discount_name = max(applicable_discounts, key=applicable_discounts.get)
    discount_amount = applicable_discounts[discount_name]
    print(f"Discount applied ({discount_name}): ${discount_amount}")
    total_amount -= discount_amount

print(f"\nShipping Fee: ${shipping_fee}")
print(f"Gift Wrap Fee: ${gift_wrap_fee}")

total_amount += shipping_fee + gift_wrap_fee
print(f"\nTotal: ${total_amount}")
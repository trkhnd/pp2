import re
import json

# Read receipt text from raw.txt
with open("raw.txt", "r", encoding="utf-8") as file:
    receipt = file.read()


# Convert price string like '1 200,00' -> 1200.00
def to_float(price_text):
    return float(price_text.replace(" ", "").replace(",", "."))


# 1. Extract all prices from the receipt
all_prices = re.findall(r'\b\d{1,3}(?: \d{3})*,\d{2}\b', receipt)

# 2. Find all product names
# Matches:
# 1.
# Product name
product_names = re.findall(r'\d+\.\s*\n([^\n]+)', receipt)

# Extract quantity and unit price like:
# 2,000 x 154,00
quantity_price_matches = re.findall(r'([\d,]+)\s*x\s*([\d ]+,\d{2})', receipt)

# Extract item totals after the word "Стоимость"
item_totals = re.findall(r'Стоимость\s*\n([\d ]+,\d{2})', receipt)

# 3. Calculate total amount
calculated_total = sum(to_float(price) for price in item_totals)

# 4. Extract date and time information
datetime_match = re.search(
    r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})',
    receipt
)

if datetime_match:
    date = datetime_match.group(1)
    time = datetime_match.group(2)
else:
    date = None
    time = None

# 5. Find payment method
payment_match = re.search(r'(Банковская карта|Наличные|Карта)', receipt)
payment_method = payment_match.group(1) if payment_match else None

# Extract receipt total from:
# ИТОГО:
# 18 009,00
total_match = re.search(r'ИТОГО:\s*\n([\d ]+,\d{2})', receipt)
receipt_total = to_float(total_match.group(1)) if total_match else None

# 6. Create structured output
products = []
count = min(len(product_names), len(quantity_price_matches), len(item_totals))

for i in range(count):
    quantity = float(quantity_price_matches[i][0].replace(",", "."))
    unit_price = to_float(quantity_price_matches[i][1])
    line_total = to_float(item_totals[i])

    products.append({
        "name": product_names[i],
        "quantity": quantity,
        "unit_price": unit_price,
        "line_total": line_total
    })

parsed_data = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "all_prices": all_prices,
    "products": products,
    "calculated_total": round(calculated_total, 2),
    "receipt_total": round(receipt_total, 2) if receipt_total is not None else None,
    "totals_match": round(calculated_total, 2) == round(receipt_total, 2) if receipt_total is not None else False
}

# Print readable output
print("RECEIPT PARSING RESULT")
print("-" * 50)
print(f"Date: {date}")
print(f"Time: {time}")
print(f"Payment method: {payment_method}")
print()

print("Products:")
for item in products:
    print(
        f"{item['name']} | "
        f"Qty: {item['quantity']} | "
        f"Unit price: {item['unit_price']} | "
        f"Total: {item['line_total']}"
    )

print()
print("All prices found:")
for price in all_prices:
    print(price)

print()
print(f"Calculated total: {parsed_data['calculated_total']}")
print(f"Receipt total: {parsed_data['receipt_total']}")
print(f"Totals match: {parsed_data['totals_match']}")

print()
print("JSON OUTPUT:")
print(json.dumps(parsed_data, ensure_ascii=False, indent=4))

# Save JSON to file
with open("parsed_receipt.json", "w", encoding="utf-8") as json_file:
    json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)
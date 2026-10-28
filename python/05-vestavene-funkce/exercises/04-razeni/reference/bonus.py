products = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def sort_by_category_and_price(products):
    ordered = sorted(products, key=lambda p: (p["category"], -p["price"]))
    return [p["name"] for p in ordered]


print(sort_by_category_and_price(products))
print(sort_by_category_and_price([]))

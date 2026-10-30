products = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def value(product):
    return product["price"] * product["qty"]


def total_value(products):
    return sum(value(p) for p in products)


def most_valuable(products):
    best = max(products, key=value, default=None)
    return best["name"] if best else None


def sorted_by_value(products):
    return [p["name"] for p in sorted(products, key=value, reverse=True)]


def categories(products):
    return sorted({p["category"] for p in products})


def any_out_of_stock(products):
    return any(p["qty"] == 0 for p in products)


for stock in [products, []]:
    print(total_value(stock))
    print(most_valuable(stock))
    print(sorted_by_value(stock))
    print(categories(stock))
    print(any_out_of_stock(stock))

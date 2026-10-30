products = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def categories(products):
    return sorted({p["category"] for p in products})


def price(product):
    return product["price"]


def cheapest_in(products, category):
    in_category = (p for p in products if p["category"] == category)
    return min(in_category, key=price)["name"]


def cheapest_by_category(products):
    return {category: cheapest_in(products, category) for category in categories(products)}


def price_stats(products):
    if not products:
        return None
    prices = [price(p) for p in products]
    return min(prices), max(prices), round(sum(prices) / len(prices), 2)


for stock in [products, []]:
    print(cheapest_by_category(stock))
    print(price_stats(stock))

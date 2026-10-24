products = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def restock(products, name, amount):
    for product in products:
        if product["name"] == name:
            product["qty"] += amount
            return True
    return False


def cheapest_by_category(products):
    cheapest = {}
    for product in products:
        current = cheapest.get(product["category"])
        if current is None or product["price"] < current["price"]:
            cheapest[product["category"]] = product

    names = {}
    for category, product in cheapest.items():
        names[category] = product["name"]
    return names


print(restock(products, "Mýdlo", 20), products[2]["qty"])
print(restock(products, "Pivo", 5))
print(cheapest_by_category(products))
print(cheapest_by_category([]))

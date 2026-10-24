products = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def total_value(products):
    total = 0
    for product in products:
        total += product["price"] * product["qty"]
    return total


def low_stock(products, limit=5):
    names = []
    for product in products:
        if product["qty"] < limit:
            names.append(product["name"])
    return names


def by_category(products):
    groups = {}
    for product in products:
        category = product["category"]
        if category not in groups:
            groups[category] = []
        groups[category].append(product["name"])
    return groups


def print_report(products):
    print(f"{'Název':<10}{'Kategorie':<12}{'Cena':>8}{'Ks':>5}{'Hodnota':>10}")
    for product in products:
        value = product["price"] * product["qty"]
        print(
            f"{product['name']:<10}{product['category']:<12}"
            f"{product['price']:>8.2f}{product['qty']:>5}{value:>10.2f}"
        )
    print(f"{'Celkem':<35}{total_value(products):>10.2f}")


print_report(products)
print(low_stock(products), low_stock(products, 1), low_stock(products, 0))
print(by_category(products))
print_report([])
print(low_stock([]), by_category([]))

products = [
    { "name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10 },
    { "name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3 },
    { "name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0 },
    { "name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4 },
    { "name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6 },
]


def total_value(products):
    total_price = 0
    for product in products:
        price = product["price"]
        qty = product["qty"]

        total_price += price * qty

    return total_price


def low_stock(products, limit=5):
    result = []

    for product in products:
        qty = product["qty"]

        if qty < limit:
            result.append(product)

    return [product["name"] for product in result]


def by_category(products):
    result = dict()

    for product in products:
        category = product["category"]
        result.setdefault(category, [])
        result[category].append(product)

    return {
        category: [product["name"] for product in products] for category, products in result.items()
    }


def print_report(products):
    total_price = total_value(products)

    print(f"{"Název":12}{"Kategorie":12}{"Cena":>12}{"Ks":>12}{"Hodnota":>12}")

    for product in products:
        name = product["name"]
        category = product["category"]
        qty = product["qty"]
        price = product["price"]

        print(f"{name:12}{category:12}{price:>12.2f}{qty:>12}{(price * qty):>12.2f}")

    print(f"Cena: {f"{total_price}":>54}")


def restock(products, name, amount):
    for product in products:
        if product["name"] == name:
            product["qty"] += amount
            return True

    return False


def cheapest_by_category(products):
    result = dict()

    for product in products:
        category = product["category"]

        if result.get(category) is None:
            result[category] = product

        if result.get(category, dict()).get("price", 0) > product["price"]:
            result[category] = product

    return {
        product["category"]: product["name"] for product in result.values()
    }


# print(cheapest_by_category(products))
print(by_category(products))

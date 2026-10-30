PRODUCTS = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def total_value(products):
    return sum(product["price"] * product["qty"] for product in products)


# print(total_value(PRODUCTS))


def most_valuable(products):
    if not products:
        return None

    valuable = max(products, key=lambda product: product["price"] * product["qty"])

    return valuable["name"]


# print(most_valuable(PRODUCTS))


def sorted_by_value(products):
    ordered = sorted(
        products,
        key=lambda product: (
            -(product["price"] * product["qty"]),
            product["name"].lower(),
        ),
    )
    return [product["name"] for product in ordered]


print(sorted_by_value(PRODUCTS))


def categories(products):
    return sorted({product["category"] for product in products}, key=str.lower)


# print(categories(PRODUCTS))


def any_out_of_stock(products):
    return any(product["qty"] == 0 for product in products)


print(any_out_of_stock(PRODUCTS))
print(any_out_of_stock([]))


def cheapest_by_category(products):
    def cheapest_in(category):
        filtered = filter(lambda product: product["category"] == category, products)
        cheapest = min(filtered, key=lambda product: product["price"], default=None)

        return cheapest["name"] if cheapest else None

    return {category: cheapest_in(category) for category in categories(products)}


print(cheapest_by_category(PRODUCTS))


def price_stats(products):
    if not products:
        return None

    summary = sum(product["price"] for product in products)
    max_price = max(product["price"] for product in products)
    min_price = min(product["price"] for product in products)
    average_price = summary / len(products)

    return (
        min_price,
        max_price,
        round(average_price, 2),
    )


print(price_stats(PRODUCTS))

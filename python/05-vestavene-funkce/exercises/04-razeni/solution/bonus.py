products = [
    {"name": "Mléko", "category": "potraviny", "price": 24.9, "qty": 10},
    {"name": "Chléb", "category": "potraviny", "price": 39.0, "qty": 3},
    {"name": "Mýdlo", "category": "drogerie", "price": 19.5, "qty": 0},
    {"name": "Šampon", "category": "drogerie", "price": 89.0, "qty": 4},
    {"name": "Káva", "category": "potraviny", "price": 149.0, "qty": 6},
]


def sort_products_by_category(products: list):
    return [
        p["name"]
        for p in sorted(
            products,
            key=lambda product: (product["category"].lower(), product["price"] * -1),
        )
    ]


print(sort_products_by_category(products))

def calculate_price(price: float, /, discount: float, *, currency="Kč"):
    discount_factor = discount / 100
    result = price - (price * discount_factor)

    return f"{result:0.1f} {currency}"


price = float(input("Zadej cenu: "))
discount = float(input("Zadej slevu (%): "))
currency = input("Zadej menu: ") or None

calculated_price = 0

if currency:
    calculated_price = calculate_price(
        price,
        discount,
        currency=currency
    )
else:
    calculated_price = calculate_price(price, discount)

print(f"{calculated_price}")

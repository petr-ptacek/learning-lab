def calculate_price(price, /, discount, *, currency="Kč"):
    result = price - price * discount / 100
    return f"{result:.1f} {currency}"


price = float(input("Zadej cenu: "))
discount = float(input("Zadej slevu (%): "))

print(calculate_price(price, discount))
print(calculate_price(price, discount=discount, currency="EUR"))

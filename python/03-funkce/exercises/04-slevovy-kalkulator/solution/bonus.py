def calculate_price(price: float, /, discount: float, *, currency="Kč", vat=0):
    discount_factor = discount / 100
    vat_factor = vat / 100 if vat > 0 else 0

    result = (price - (price * discount_factor))
    result += (vat_factor * result)

    return f"{result:0.1f} {currency}"


price = float(input("Zadej cenu: "))
discount = float(input("Zadej slevu (%): "))
vat = float(input("Zadej vat (%): "))

calculated_price = calculate_price(price, discount, vat=vat)

print(f"{calculated_price}")

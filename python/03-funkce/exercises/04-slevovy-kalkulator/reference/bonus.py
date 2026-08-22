def calculate_price(price, /, discount, *, currency="Kč", vat=0):
    price_after_discount = price - price * discount / 100
    price_with_vat = price_after_discount + price_after_discount * vat / 100
    return f"{price_with_vat:.1f} {currency}"


price = float(input("Zadej cenu: "))
discount = float(input("Zadej slevu (%): "))
vat = float(input("Zadej DPH (%): "))

print(calculate_price(price, discount, vat=vat))
print(calculate_price(price, discount=discount, currency="EUR", vat=vat))

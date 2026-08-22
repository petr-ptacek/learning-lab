def format_address(street, number, city, zip_code):
    return f"{street} {number}, {zip_code} {city}"


street = input("Zadej ulici: ")
number = input("Zadej číslo: ")
city = input("Zadej město: ")
zip_code = input("Zadej PSČ: ")

print(format_address(city=city, zip_code=zip_code, street=street, number=number))

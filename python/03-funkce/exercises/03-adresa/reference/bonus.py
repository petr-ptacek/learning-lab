def format_address(street, number, city, zip_code, orientation_number=None):
    if orientation_number:
        return f"{street} {number}/{orientation_number}, {zip_code} {city}"

    return f"{street} {number}, {zip_code} {city}"


street = input("Zadej ulici: ")
number = input("Zadej číslo: ")
city = input("Zadej město: ")
zip_code = input("Zadej PSČ: ")
orientation_number = input("Zadej číslo orientační (nebo nic): ") or None

print(format_address(city=city, zip_code=zip_code, street=street, number=number, orientation_number=orientation_number))

def format_address(street, number, city, zip_code, orientation_number=None):
    if orientation_number:
        return f"{street} {number}/{orientation_number}, {zip_code} {city}"

    return f"{street} {number}, {zip_code} {city}"


street = input("Street: ")
number = input("Number: ")
city = input("City: ")
zip_code = input("Zip Code: ")
orientation_number = input("Orientation Number: ") or None

result = format_address(
    number=number,
    street=street,
    city=city,
    zip_code=zip_code,
    orientation_number=orientation_number
)

print(result)

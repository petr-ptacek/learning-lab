def format_address(street, number, city, zip_code):
    return f"{street} {number}, {zip_code} {city}"


street = input("Street: ")
number = input("Number: ")
city = input("City: ")
zip_code = input("Zip Code: ")

result = format_address(number=number, street=street, city=city, zip_code=zip_code)
print(result)

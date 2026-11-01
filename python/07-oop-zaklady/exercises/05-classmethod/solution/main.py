class Product:
    def __init__(self, name, price, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product({self.name!r}, {self.price}, {self.quantity})"

    @classmethod
    def from_csv_line(cls, line):
        chunks = [c.strip() for c in line.split(";")]
        name = chunks[0]
        price = float(chunks[1])
        quantity = int(chunks[2])

        return cls(name, price, quantity=quantity)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["name"], d["price"], quantity=d.get("quantity", 0))

    @staticmethod
    def is_valid_code(code: str) -> bool:
        return len(code) == 8 and code.isdigit()


product1 = Product("Milk", 100)
product2 = Product.from_csv_line(" Chléb ;39;0")
product3 = Product.from_dict({"name": "Coffee", "price": 100})

# print([product1, product2, product3])

# print(product1.is_valid_code("123"))
# funguje, protoze metoda je ulozena jakoby na class tride, ale nedava se ji jako prvni parametr instance, nebo cls

# print(Product.is_valid_code("12345678"))
# print(Product.is_valid_code("123456789"))
# print(Product.is_valid_code("1234567a"))

p = Product("x", 1)
print(p.is_valid_code("12345678"))
print(p.from_csv_line("A;1;1"))
# vytvori instanci
print(type(Product.from_dict), type(Product.is_valid_code))
# obe jsou classfunctions, coz je ocekavane, setreni mista, nez aby to bylo v instanci

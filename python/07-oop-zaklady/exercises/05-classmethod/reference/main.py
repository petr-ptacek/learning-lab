class Product:
    def __init__(self, name: str, price: float, quantity: int = 0) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.price!r}, {self.quantity!r})"

    # cls je třída, přes kterou se metoda zavolala. Podtřída
    # (DiscountedProduct.from_dict) tak dostane instanci podtřídy,
    # Product(...) natvrdo by vždy vyrobil Product.
    @classmethod
    def from_csv_line(cls, line: str) -> "Product":
        name, price, quantity = line.split(";")
        return cls(name.strip(), float(price), int(quantity))

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(data["name"], data["price"], data.get("quantity", 0))

    @staticmethod
    def is_valid_code(code: str) -> bool:
        return len(code) == 8 and code.isdigit()


print(Product.from_csv_line(" Chléb ;39;0"))  # Product('Chléb', 39.0, 0)
print(Product.from_dict({"name": "Sůl", "price": 12.5}))  # Product('Sůl', 12.5, 0)
print(Product.is_valid_code("12345678"), Product.is_valid_code("1234567a"))

p = Product("x", 1)
print(p.is_valid_code("12345678"))  # True: staticmethod nic nedostává
print(p.from_csv_line("A;1;1"))  # funguje, do cls se dosadí type(p), ne p
# <class 'method'> <class 'function'>: classmethod je vázaná na třídu,
# staticmethod je obyčejná funkce uložená na třídě.
print(type(Product.from_dict), type(Product.is_valid_code))

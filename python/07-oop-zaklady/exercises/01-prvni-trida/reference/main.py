class Product:
    def __init__(self, name: str, price: float, quantity: int = 0) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_value(self) -> float:
        return round(self.price * self.quantity, 2)

    def restock(self, amount: int) -> None:
        self.quantity += amount

    def sell(self, amount: int) -> bool:
        if amount > self.quantity:
            return False
        self.quantity -= amount
        return True


a = Product("Mléko", 24.9, 10)
b = Product("Chléb", 39.0)
a.sell(3)
print(a.quantity, b.quantity)  # 7 0
# False: bez __eq__ porovnává == identitu objektů (jako `is`), ne data.
print(a == Product("Mléko", 24.9, 7))
# <__main__.Product object at 0x...>: výchozí __repr__ (třída + adresa).
print(a)
# True: a.total_value() je jen zkratka za Product.total_value(a),
# instance se do self dosadí automaticky.
print(Product.total_value(a) == a.total_value())

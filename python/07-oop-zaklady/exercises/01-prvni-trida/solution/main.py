class Product:
    def __init__(self, name: str, price: float, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return round(self.price * self.quantity, 2)

    def restock(self, amount: int):
        self.quantity += amount

    def sell(self, amount: int):
        if self.quantity >= amount:
            self.quantity -= amount
            return True

        return False

    def apply_discount(self, percent: int):
        discount = self.price * (percent / 100)
        self.price = round(self.price - discount, 2)


a = Product("Mléko", 24.9, 10)
b = Product("Chléb", 39.0)
a.sell(3)
print(a.quantity, b.quantity)
# 7, 0
print(a == Product("Mléko", 24.9, 7))
# False - porovnavaji se reference
print(a)
# pointer

print(Product.total_value(a) == a.total_value())
# true, Product.total_value, je instnacni metoda a jako prvni argument dostane instnaci, z ni pak cte dane attributy, a.total_value se vola na instanci, takze to cte z dane instance

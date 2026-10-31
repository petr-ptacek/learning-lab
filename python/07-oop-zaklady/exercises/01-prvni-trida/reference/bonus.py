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

    def apply_discount(self, percent: float) -> None:
        self.price = round(self.price * (1 - percent / 100), 2)


q = Product("Káva", 189.0, 3)
q.apply_discount(10)
print(q.price, q.total_value())  # 170.1 510.3


class Broken:
    def hello():
        return "ahoj"


# Broken().hello() se přeloží na Broken.hello(instance). Tím jediným
# „given“ argumentem je instance, kterou Python dosazuje do self, jenže
# hello() žádný parametr nemá.
# TypeError: Broken.hello() takes 0 positional arguments but 1 was given
Broken().hello()

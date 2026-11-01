class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency


m = Money(249.9)
print(m)
print([m, Money(10, "EUR")])
print(f"Celkem: {m}, ladění: {m!r}")
print(m == Money(249.9))

class Money:
    def __init__(self, amount, currency="CZK"):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        return self.amount == other.amount and self.currency == other.currency

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        if other.currency != self.currency:
            return NotImplemented

        return Money(round(self.amount + other.amount, 2), self.currency)


# [Money(100)]

print(Money(100))
print(Money(100, "USD"))
print([Money(100, "USD"), Money(100, "CZK")])
print(Money(100, "USD") == Money(100, "USD"))
print(Money(100, "USD") + Money(100, "USD"))
print(Money(100, "USD") + 5)

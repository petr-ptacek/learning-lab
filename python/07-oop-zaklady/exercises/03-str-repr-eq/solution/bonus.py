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

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        if other.currency != self.currency:
            return NotImplemented

        return self.amount < other.amount

    def __bool__(self):
        return bool(self.amount)

    def __radd__(self, amount: int):
        if amount == 0:
            return self + Money(0, self.currency)

        return NotImplemented


moneys = [Money(8), Money(0), Money(6), Money(4)]

# print({Money(1), Money(2), Money(3), Money(4), Money(1), Money(2)})
# unable to use Money as set element

# print(sorted(moneys))
# print(max(moneys))
# print(min(moneys))
print(sum(moneys))

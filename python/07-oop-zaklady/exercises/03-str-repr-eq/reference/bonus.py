class Money:
    def __init__(self, amount: float, currency: str = "CZK") -> None:
        self.amount = amount
        self.currency = currency

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)

    # Když třída definuje __eq__ bez __hash__, Python nastaví
    # __hash__ = None, takže {Money(1)} hlásí „unhashable type“.
    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return self.amount < other.amount

    def __bool__(self) -> bool:
        return self.amount != 0

    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(round(self.amount + other.amount, 2), self.currency)

    # sum() začíná od 0: první krok je 0 + Money(...), int.__add__ vrátí
    # NotImplemented a Python zkusí Money.__radd__(0).
    def __radd__(self, other: object) -> "Money":
        if other == 0:
            return self
        return NotImplemented


prices = [Money(30), Money(10.5), Money(20)]
print(len({Money(1), Money(1), Money(2, "EUR")}))  # 2
print(sorted(prices))
print(max(prices), min(prices))  # 30.00 CZK 10.50 CZK
print(bool(Money(0)), bool(Money(0.01)))  # False True
print(sum(prices))  # 60.50 CZK

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

    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(round(self.amount + other.amount, 2), self.currency)


m = Money(249.9)
print(m)  # 249.90 CZK
# Seznam nemá vlastní __str__, vypíše svůj __repr__ a ten volá repr
# prvků: u obsahu kontejneru musí být vidět, co přesně v něm je.
print([m, Money(10, "EUR")])  # [Money(249.9, 'CZK'), Money(10, 'EUR')]
print(f"Celkem: {m}, ladění: {m!r}")
print(m == Money(249.9))  # True (bez __eq__ by bylo False)
print(Money(0.1) + Money(0.2))  # 0.30 CZK

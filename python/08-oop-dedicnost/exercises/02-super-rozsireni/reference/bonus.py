class BankAccount:
    fee = 0

    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner
        self.balance = balance
        self.history: list[tuple[str, float]] = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.history.append(("deposit", amount))

    def can_withdraw(self, total: float) -> bool:  # háček pro podtřídy
        return total <= self.balance

    def withdraw(self, amount: float) -> bool:
        total = amount + self.fee
        if not self.can_withdraw(total):
            return False
        self.balance -= total
        self.history.append(("withdraw", total))
        return True

    def transfer(self, to: "BankAccount", amount: float) -> bool:
        if not self.withdraw(amount):  # pravidla všech typů hlídá withdraw
            return False
        to.deposit(amount)
        return True

    @classmethod
    def open(cls, owner: str, initial: float) -> "BankAccount":
        return cls(owner, initial)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.owner!r}, {self.balance!r})"


class SavingsAccount(BankAccount):
    interest_rate = 0.02
    max_withdrawals = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.withdrawals = 0

    def add_interest(self) -> None:
        self.balance = round(self.balance * (1 + self.interest_rate), 2)

    def withdraw(self, amount: float) -> bool:
        if self.withdrawals >= self.max_withdrawals:
            return False
        if not super().withdraw(amount):  # historii zapíše rodič
            return False
        self.withdrawals += 1
        return True


class CheckingAccount(BankAccount):
    fee = 5

    def __init__(self, *args, overdraft: float = 1000, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.overdraft = overdraft

    def can_withdraw(self, total: float) -> bool:  # přepíše jen podmínku
        return total <= self.balance + self.overdraft


s = SavingsAccount("Petr", 1000)
s.deposit(200)
s.withdraw(100)
s.withdraw(5000)
print(s.history)  # [('deposit', 200), ('withdraw', 100)]

c = CheckingAccount("Eva", 100)
c.withdraw(500)
c.withdraw(600)
print(c.history)  # [('withdraw', 505)]

a = BankAccount("Anna", 1000)
c2 = CheckingAccount("Jan", 0)
print(a.transfer(c2, 300), c2.transfer(a, 1000), c2.transfer(a, 1000))  # True True False
print(a, c2)  # BankAccount('Anna', 1700) CheckingAccount('Jan', -705)

s2 = SavingsAccount("Lea", 1000)
print([s2.transfer(a, 10) for _ in range(4)])  # [True, True, True, False]

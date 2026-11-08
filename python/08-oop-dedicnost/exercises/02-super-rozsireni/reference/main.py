class BankAccount:
    fee = 0

    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        total = amount + self.fee
        if total > self.balance:
            return False
        self.balance -= total
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
        if not super().withdraw(amount):
            return False
        self.withdrawals += 1
        return True


class CheckingAccount(BankAccount):
    fee = 5

    def __init__(self, *args, overdraft: float = 1000, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.overdraft = overdraft

    # Celé přepsání: musel jsem zkopírovat výpočet poplatku i odečtení.
    # Kdyby rodič začal třeba zapisovat historii, tady by chyběla.
    def withdraw(self, amount: float) -> bool:
        total = amount + self.fee
        if total > self.balance + self.overdraft:
            return False
        self.balance -= total
        return True


print(SavingsAccount.open("Petr", 1000))  # SavingsAccount('Petr', 1000)
print(BankAccount.fee, CheckingAccount.fee, SavingsAccount.fee)  # 0 5 0 (SavingsAccount dědí 0)
print(type(CheckingAccount.open("Jan", 50)).__name__)  # CheckingAccount: cls je CheckingAccount

s = SavingsAccount.open("Petr", 1000)
s.add_interest()
print([s.withdraw(100), s.withdraw(5000), s.withdraw(100), s.withdraw(100), s.withdraw(100)])
print(s.balance)  # 720.0

c = CheckingAccount("Eva", 100)
print(c.withdraw(500), c.withdraw(600), c.withdraw(590), c)  # True False True CheckingAccount('Eva', -1000)

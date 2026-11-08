class BankAccount:
    fee: float = 0

    def __init__(self, owner: str, balance: float = 0):
        self.owner: str = owner
        self.balance: float = balance
        self.history: list[tuple[str, float]] = []

    def deposit(self, amount: float):
        self.balance += amount
        self.history.append(("deposit", amount))

    def can_withdraw(self, amount: float):
        return self.balance - (amount + self.fee) >= 0

    def withdraw(self, amount: float):
        if not self.can_withdraw(amount):
            return False

        value = amount + self.fee
        self.balance -= value
        self.history.append(("withdraw", value))

        return True

    def transfer(self, to: "BankAccount", amount: float):
        if not self.withdraw(amount):
            return False

        to.deposit(amount)

        return True

    @classmethod
    def open(cls, owner: str, initial_balance: float):
        return cls(owner, initial_balance)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.owner!r}, {self.balance})"


class SavingsAccount(BankAccount):
    interest_rate: float = 0.02
    withdraw_limit = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_withdraw_count = 0

    def add_interest(self):
        self.balance += round(self.balance * self.interest_rate, 2)

    def can_withdraw(self, amount: float):
        return (
            self.current_withdraw_count + 1 <= self.withdraw_limit
            and super().can_withdraw(amount)
        )

    def withdraw(self, amount: float):
        success = super().withdraw(amount)

        if success:
            self.current_withdraw_count += 1

        return success


class CheckingAccount(BankAccount):
    fee: float = 5

    def __init__(self, *args, overdraft: float = 1_000, **kwargs):
        super().__init__(*args, **kwargs)
        self.overdraft = overdraft

    def can_withdraw(self, amount: float):
        return (self.balance + self.overdraft) - (amount + self.fee) >= 0


print(SavingsAccount("Petr", 1000))
# SavingsAccount(Petr,1000)
print(BankAccount.fee, CheckingAccount.fee, SavingsAccount.fee)
# 0, 5, 0
print(type(CheckingAccount.open("Jan", 50)).__name__)
# CheckingAccount - vola se to s cls nastavenou na CheckingAccount

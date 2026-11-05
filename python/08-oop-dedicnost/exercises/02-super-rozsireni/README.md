# 02 — `super()`: rozšířit, nebo přepsat?

Podtřída má dvě možnosti: metodu rodiče **rozšířit** (něco udělá navíc
a zbytek nechá na `super()`), nebo ji **přepsat** celou. A třetí, kterou
Django používá pořád: rodič čte **atribut třídy** (`fee`,
`template_name`, `paginate_by`) a podtřída jen změní jeho hodnotu.

Teorie: [`docs/INHERITANCE_AND_SUPER.md`](../../../docs/INHERITANCE_AND_SUPER.md).

## Požadavky

- `BankAccount(owner, balance=0)`:
  - atribut třídy `fee = 0` (poplatek za výběr),
  - `deposit(amount)`,
  - `withdraw(amount)` → odečte `amount + self.fee` a vrátí `True`;
    když by šel zůstatek do mínusu, nic nezmění a vrátí `False`,
  - `__repr__` → `BankAccount('Anna', 500)`, jméno třídy přes
    `type(self).__name__`,
  - `@classmethod open(cls, owner, initial)` → nový účet přes `cls(...)`.
- `SavingsAccount(BankAccount)`:
  - atribut třídy `interest_rate = 0.02`, `add_interest()` připíše úrok
    (zaokrouhli na 2 místa),
  - nejvýš **3 výběry**: `withdraw` přepiš tak, že limit zkontroluje,
    samotný výběr nechá na `super().withdraw(...)` a do limitu počítá
    jen **úspěšné** výběry.
- `CheckingAccount(owner, balance=0, overdraft=1000)`:
  - `fee = 5` (jen změna atributu třídy, žádný nový kód pro poplatek),
  - smí jít do mínusu, nejvýš o `overdraft`.
- **Otázka:** u `CheckingAccount` nejde výběr jen „rozšířit“, podmínka
  v rodiči je jiná. Napiš ho zatím přepsáním celé metody. Co všechno
  jsi musel zkopírovat z rodiče? Co by se stalo, kdyby se rodičovský
  `withdraw` později změnil (třeba začal zapisovat historii)? Bonus
  ukáže lepší cestu.
- **Předpověď:** co vypíše?

  ```python
  print(SavingsAccount.open("Petr", 1000))
  print(BankAccount.fee, CheckingAccount.fee, SavingsAccount.fee)
  print(type(CheckingAccount.open("Jan", 50)).__name__)
  ```

### Příklady vstup/výstup

Postupně za sebou, `a = BankAccount("Anna", 1000)`:

| Kód                          | Výsledek                       |
|------------------------------|--------------------------------|
| `a.withdraw(300)`, `a.balance` | `True`, `700`                |
| `a.withdraw(800)`, `a.balance` | `False`, `700`               |
| `a.withdraw(700)`, `a.balance` | `True`, `0` (přesně na nulu) |
| `a.withdraw(0)`              | `True`                         |
| `a.deposit(500)`, `a`        | `BankAccount('Anna', 500)`     |
| `BankAccount("Nula")`        | `BankAccount('Nula', 0)`       |

`s = SavingsAccount.open("Petr", 1000)`:

| Kód                                   | Výsledek                         |
|---------------------------------------|----------------------------------|
| `s`                                   | `SavingsAccount('Petr', 1000)`   |
| `s.add_interest()`, `s.balance`       | `1020.0`                         |
| `s.withdraw(100)`                     | `True`                           |
| `s.withdraw(5000)`                    | `False` (nepočítá se do limitu)  |
| `s.withdraw(100)`, `s.withdraw(100)`  | `True`, `True`                   |
| `s.withdraw(100)`                     | `False` (čtvrtý výběr)           |
| `s.balance`                           | `720.0`                          |

`c = CheckingAccount("Eva", 100)`:

| Kód                                   | Výsledek                         |
|---------------------------------------|----------------------------------|
| `c.withdraw(500)`, `c.balance`        | `True`, `-405` (500 + poplatek 5) |
| `c.withdraw(600)`, `c.balance`        | `False`, `-405`                  |
| `c.withdraw(590)`, `c.balance`        | `True`, `-1000` (přesně na limit) |
| `c.withdraw(1)`                       | `False`                          |
| `c`                                   | `CheckingAccount('Eva', -1000)`  |
| `CheckingAccount("Ota", 0, overdraft=0).withdraw(1)` | `False`           |
| `CheckingAccount.open("Jan", 50)`     | `CheckingAccount('Jan', 50)`     |

## Bonus

- `history`: každý účet si vede seznam transakcí, `("deposit", částka)`
  a `("withdraw", částka_včetně_poplatku)`. Zapisuje se **jen**
  v `BankAccount`. `SavingsAccount` musí historii dostat automaticky
  díky `super()`, bez jediného řádku navíc.
- Vyzkoušej si historii u svého `CheckingAccount` s přepsaným
  `withdraw`. Proč je prázdná? Oprav to tak, že v rodiči vytáhneš
  podmínku do samostatné metody `can_withdraw(total)` a
  `CheckingAccount` přepíše **jen ji**. `withdraw` pak nepřepisuje vůbec.
  (Stejný princip jako u Django CBV: přepisuješ malé „háčky“ typu
  `get_queryset`, ne celou metodu `get`.)
- `transfer(to, amount)` v `BankAccount`: výběr z `self`, vklad na `to`,
  `True` / `False`. Musí fungovat mezi **všemi** typy účtů a respektovat
  jejich pravidla (poplatek, přečerpání, limit výběrů), bez jediného
  `isinstance`.

### Příklady vstup/výstup (bonus)

| Kód                                                                 | Výsledek                                   |
|---------------------------------------------------------------------|--------------------------------------------|
| `s = SavingsAccount("Petr", 1000)`, `s.deposit(200)`, `s.withdraw(100)`, `s.withdraw(5000)`, `s.history` | `[('deposit', 200), ('withdraw', 100)]` |
| `c = CheckingAccount("Eva", 100)`, `c.withdraw(500)`, `c.withdraw(600)`, `c.history` | `[('withdraw', 505)]`           |
| `BankAccount("Nikdo").history`                                      | `[]`                                       |

Postupně, `a = BankAccount("Anna", 1000)`, `c2 = CheckingAccount("Jan", 0)`:

| Kód                          | Výsledek                                                     |
|------------------------------|--------------------------------------------------------------|
| `a.transfer(c2, 300)`, `(a, c2)` | `True`, `(BankAccount('Anna', 700), CheckingAccount('Jan', 300))` |
| `c2.transfer(a, 1000)`, `(a, c2)` | `True`, `(BankAccount('Anna', 1700), CheckingAccount('Jan', -705))` |
| `c2.transfer(a, 1000)`       | `False` (překročil by přečerpání)                            |
| `a.history`                  | `[('withdraw', 300), ('deposit', 1000)]`                     |
| `c2.history`                 | `[('deposit', 300), ('withdraw', 1005)]`                     |
| `s2 = SavingsAccount("Lea", 1000)`, `[s2.transfer(a, 10) for _ in range(4)]` | `[True, True, True, False]` |

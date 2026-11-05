# 05 — Mixiny a MRO

Mixin je malá třída s jednou schopností, kterou „přimícháš“ do jiné
třídy vícenásobnou dědičností. Django views jsou na tom postavené:
`class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, TemplateView)`.
Aby to fungovalo, musíš vědět, v jakém pořadí Python třídy prochází
(MRO) a kam vlastně skočí `super()`.

Teorie: [`docs/MULTIPLE_INHERITANCE_AND_MIXINS.md`](../../../docs/MULTIPLE_INHERITANCE_AND_MIXINS.md).

## Požadavky

**Mixiny se schopností:**

- `ReprMixin` — generický `__repr__` ze všech atributů instance
  (`vars(self)`): `Product(name='Mléko', price=24.9)`. Jméno třídy přes
  `type(self).__name__`.
- `JsonMixin` — `to_json()` → JSON string ze všech atributů instance,
  české znaky bez escapování.
- Mixiny nemají `__init__` ani vlastní data, jen metody.
- Použij je na dvě nesouvisející třídy: `Product(name, price)`
  a `Customer(name, email, vip=False)`. Ani jedna nemá vlastní
  `__repr__` ani `to_json`.

**Mini class-based views:**

- `View` s metodami `dispatch(request)` → vrátí `self.get(request)`
  a `get(request)` → `"200 OK"`. `request` je obyčejný dict.
- `LoginRequiredMixin.dispatch(request)`: když v requestu chybí
  `"user"` (nebo je `None`), vrátí `"302 /login/"`. Jinak pokračuje
  přes `super().dispatch(request)`.
- `StaffRequiredMixin.dispatch(request)`: když `request` nemá
  `"is_staff": True`, vrátí `"403 Forbidden"`, jinak `super().dispatch(...)`.
- `AdminView(LoginRequiredMixin, StaffRequiredMixin, View)` s vlastním
  `get` → `"200 Admin pro anna"`.
- `ProfileView(LoginRequiredMixin, View)` → `"200 Profil petr"`.
- **Předpověď:** napiš si do komentáře, pak ověř:
  1. `[c.__name__ for c in AdminView.__mro__]`
  2. Mixin dědí jen z `object` a ten žádný `dispatch` nemá. Kam tedy
     v `LoginRequiredMixin` skočí `super().dispatch(...)`?
  3. Co se změní, když v hlavičce prohodíš oba mixiny
     (`StaffRequiredMixin, LoginRequiredMixin, View`)? Vrací pak
     nepřihlášenému uživateli stejnou odpověď?
  4. Co se stane s `class WrongView(View, LoginRequiredMixin)`, tedy
     s mixinem **za** základní třídou? Proč se mixiny píšou vlevo?

### Příklady vstup/výstup

| Kód                                                    | Výsledek                                                   |
|--------------------------------------------------------|------------------------------------------------------------|
| `Product("Mléko", 24.9)`                               | `Product(name='Mléko', price=24.9)`                        |
| `Product("Mléko", 24.9).to_json()`                     | `'{"name": "Mléko", "price": 24.9}'`                       |
| `Customer("Anna", "anna@example.cz")`                  | `Customer(name='Anna', email='anna@example.cz', vip=False)` |
| `Customer("Žofie", "z@example.cz", vip=True).to_json()` | `'{"name": "Žofie", "email": "z@example.cz", "vip": true}'` |
| `[c.__name__ for c in Product.__mro__]`                | `['Product', 'ReprMixin', 'JsonMixin', 'object']`          |

| Kód                                                          | Výsledek                  |
|--------------------------------------------------------------|---------------------------|
| `View().dispatch({})`                                        | `'200 OK'`                |
| `AdminView().dispatch({})`                                   | `'302 /login/'`           |
| `AdminView().dispatch({"user": "anna"})`                     | `'403 Forbidden'`         |
| `AdminView().dispatch({"is_staff": True})`                   | `'302 /login/'`           |
| `AdminView().dispatch({"user": "anna", "is_staff": True})`   | `'200 Admin pro anna'`    |
| `ProfileView().dispatch({"user": "petr"})`                   | `'200 Profil petr'`       |
| `ProfileView().dispatch({})`                                 | `'302 /login/'`           |
| `[c.__name__ for c in AdminView.__mro__]`                    | `['AdminView', 'LoginRequiredMixin', 'StaffRequiredMixin', 'View', 'object']` |
| prohozené mixiny: `.dispatch({})`                            | `'403 Forbidden'`         |
| prohozené mixiny: `.dispatch({"is_staff": True})`            | `'302 /login/'`           |
| `WrongView().dispatch({})` (s `get` → `"200 tajné"`)         | `'200 tajné'` (kontrola se vůbec nespustila) |
| `LoginRequiredMixin().dispatch({"user": "x"})`               | `AttributeError: 'super' object has no attribute 'dispatch'` |

## Bonus

- **Diamant.** `A.hello()` vrací `["A"]`, `B(A)` a `C(A)` vrací
  `["B", *super().hello()]` / `["C", *super().hello()]`, `D(B, C)`
  vrací `["D", *super().hello()]`. Předpověz `D().hello()` a `D.mro()`.
  Proč se `A` objeví jen **jednou** a proč je po `B` rovnou `C`, i když
  `B` z `C` vůbec nedědí? Co to říká o tom, kam míří `super()`?
- **Nekonzistentní MRO.** Zkus `class X(A, B): pass`. Přečti chybu
  a vysvětli, proč Python odmítne pořadí, ve kterém je rodič před
  vlastním potomkem. Jak hlavičku opravit?
- **Kooperativní `save()`.** `Model` má `__init__` s `self.log = []`
  a `save()` → zapíše `"uloženo"`. Dva mixiny:
  - `TimestampMixin.save()`: nastaví `self.updated_at = "2026-11-05"`,
    zapíše `"timestamp"` a pokračuje `super().save()`,
  - `ValidationMixin.save()`: když chybí `title` (prázdný), zapíše
    `"chyba: chybí title"` a **skončí** bez `super()`. Jinak zapíše
    `"validace ok"` a pokračuje.

  `Article(TimestampMixin, ValidationMixin, Model)` s parametrem
  `title=""`. Porovnej s pořadím `ValidationMixin, TimestampMixin`:
  které pořadí je správné, aby se u neplatného článku nenastavil
  `updated_at`?

### Příklady vstup/výstup (bonus)

| Kód                                       | Výsledek                                                                |
|-------------------------------------------|-------------------------------------------------------------------------|
| `B().hello()`, `C().hello()`              | `['B', 'A']`, `['C', 'A']`                                              |
| `D().hello()`                             | `['D', 'B', 'C', 'A']`                                                  |
| `[c.__name__ for c in D.mro()]`           | `['D', 'B', 'C', 'A', 'object']`                                        |
| `class X(A, B): pass`                     | `TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B` |
| `class Y(B, A)`, `[c.__name__ for c in Y.mro()]` | `['Y', 'B', 'A', 'object']`                                      |

| Kód                                                        | Výsledek                                         |
|------------------------------------------------------------|--------------------------------------------------|
| `a = Article("Úvod")`, `a.save()`, `a.log`                 | `['timestamp', 'validace ok', 'uloženo']`        |
| `b = Article()`, `b.save()`, `b.log`                       | `['timestamp', 'chyba: chybí title']`            |
| `hasattr(b, "updated_at")`                                 | `True` (neuložený článek má čas změny)           |
| s pořadím `ValidationMixin, TimestampMixin`: `save()` bez title, `log` | `['chyba: chybí title']`             |
| …a `hasattr(..., "updated_at")`                            | `False`                                          |
| …s `title="Ok"`: `log`                                     | `['validace ok', 'timestamp', 'uloženo']`        |

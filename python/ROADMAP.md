# python — Roadmap

Plán konceptů v doporučeném pořadí. Zaškrtnuto = koncept zvládnutý (teorie
prostudovaná + cvičení vyřešená), ne jen založený.

- [x] 01-zaklady
- [x] 02-podminky-cykly
- [x] 03-funkce — vlastní funkce (`def`, parametry, návratové hodnoty,
      scope) — vestavěné funkce Pythonu jsou samostatný koncept, viz
      05-vestavene-funkce
- [x] 04-datove-struktury
- [x] 05-vestavene-funkce — `len`, `min`/`max`, `sum`, `sorted`, `enumerate`,
      `zip`, `map`, `filter`, `any`/`all` (staví na 04-datove-struktury)
- [x] 06-generatory-iteratory — `yield`, generátorové výrazy, iterátory,
      `next()`/`iter()` (staví na 03-funkce a 04-datove-struktury)
- [ ] 07-oop-zaklady — třída a instance, `__init__` a `self`, atributy
      instance vs. atributy třídy, metody, `@property`, `@classmethod` /
      `@staticmethod`, dunder metody (`__str__`, `__repr__`, `__eq__`,
      `__len__`, `__iter__`), `dataclass`
- [ ] 08-oop-dedicnost — dědičnost, `super()`, abstraktní základ, mixiny
      a MRO, vnořená třída (`Meta`), `__init_subclass__` a základ
      metatříd a deskriptorů: jak Django model posbírá svá pole (staví
      na 07-oop-zaklady, připravuje na Django modely a class-based views)
- [ ] 09-stringy
- [ ] 10-vyjimky
- [ ] 11-soubory
- [ ] 12-moduly-balicky
- [ ] 13-pandas — práce s tabulkovými daty: `DataFrame` / `Series`,
      načtení CSV / Excelu, filtrování, výběr sloupců, `groupby`,
      agregace, spojování tabulek, export (staví na 11-soubory
      a 12-moduly-balicky)

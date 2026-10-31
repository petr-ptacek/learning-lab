# 06 — Vlastní kontejner

Třída, která v sobě drží kolekci a chová se jako seznam: `len`, `for`,
`in`, indexy. Přesně tak funguje Django QuerySet (`len(qs)`,
`for book in qs`, `qs[:10]`, `if qs:`).

Teorie: [`docs/DUNDER_METHODS.md`](../../../docs/DUNDER_METHODS.md),
sekce 6–7. `__iter__` napiš jako generátor (`06-generatory-iteratory`).

## Požadavky

- `Song(title, seconds)`:
  - `__repr__` → `Song('Imagine', 183)`,
  - property `duration` → `"3:03"` (minuty bez úvodní nuly, sekundy
    vždy dvoumístně). Nápověda: `divmod`.
- `Playlist(name, songs=None)` — `songs` je volitelný iterable písní,
  uvnitř si ulož vlastní **nový** seznam:
  - `add(song)`,
  - `__len__`, `__iter__` (generátor), `__getitem__` (index i slice,
    stačí delegovat na seznam),
  - `__contains__(title)` — hledá podle **názvu** písně, ne podle
    objektu,
  - property `total_seconds` a `total_duration` (stejný formát jako
    `duration`, minuty můžou být víc než 59).
- **Předpověď:** co vypíše, než přidáš první píseň a potom? Proč
  funguje `if playlist:`, i když jsi nenapsal `__bool__`? Proč funguje
  `reversed`, i když jsi nenapsal `__reversed__`?

  ```python
  p = Playlist("Ráno")
  print(len(p), bool(p))
  p.add(Song("Imagine", 183))
  print(len(p), bool(p), list(reversed(p)))
  ```

### Příklady vstup/výstup

| Kód                                        | Výsledek                  |
|--------------------------------------------|---------------------------|
| `Song("Bohemian Rhapsody", 354).duration`  | `'5:54'`                  |
| `Song("Krátká", 59).duration`              | `'0:59'`                  |
| `Song("Přesně", 120).duration`             | `'2:00'`                  |
| `Song("Nic", 0).duration`                  | `'0:00'`                  |

Po `p = Playlist("Ráno")` a přidání `Song("Bohemian Rhapsody", 354)`,
`Song("Imagine", 183)`, `Song("Hey Jude", 431)`:

| Kód                                        | Výsledek                                                         |
|--------------------------------------------|------------------------------------------------------------------|
| `len(p)`                                   | `3`                                                              |
| `[s.title for s in p]`                     | `['Bohemian Rhapsody', 'Imagine', 'Hey Jude']`                   |
| `"Imagine" in p, "Yesterday" in p`         | `(True, False)`                                                  |
| `p[0]`                                     | `Song('Bohemian Rhapsody', 354)`                                 |
| `p[-1]`                                    | `Song('Hey Jude', 431)`                                          |
| `p[:2]`                                    | `[Song('Bohemian Rhapsody', 354), Song('Imagine', 183)]`         |
| `p.total_seconds, p.total_duration`        | `(968, '16:08')`                                                 |
| `max(p, key=lambda s: s.seconds).title`    | `'Hey Jude'`                                                     |
| `p[10]`                                    | `IndexError: list index out of range`                            |
| `Playlist("Prázdný").total_duration`       | `'0:00'`                                                         |
| `bool(Playlist("Prázdný"))`                | `False`                                                          |

## Bonus

- `__add__` — spojí dva playlisty do **nového**, jméno `"A + B"`.
  Původní se nemění.
- `__repr__` playlistu → `Playlist('Ráno', 3 skladeb)`.
- `__eq__` — dva playlisty jsou si rovné, když mají stejné názvy písní
  ve stejném pořadí (jméno playlistu nehraje roli).
- **Otázka:** `p[:2]` vrací obyčejný seznam, ne `Playlist`. Proč?
  Jak bys to změnil? (Stačí slovně, nebo zkus.)

### Příklady vstup/výstup (bonus)

S `p` z tabulky výše a `q = Playlist("Večer", [Song("Yesterday", 125)])`:

| Kód                                         | Výsledek                                   |
|---------------------------------------------|--------------------------------------------|
| `p + q`                                     | `Playlist('Ráno + Večer', 4 skladeb)`      |
| `(p + q).total_duration`                    | `'18:13'`                                  |
| `len(p)` po sčítání                         | `3`                                        |
| `Playlist("A", [Song("X", 1)]) == Playlist("B", [Song("X", 1)])` | `True`  |
| `Playlist("A", [Song("X", 1)]) == Playlist("A", [Song("Y", 1)])` | `False` |

# 02 — Detail uživatele podle výběru

Těžší cvičení — `useEffect` se **skutečně měnící se** závislostí, ne jen
jednorázový fetch při mountu. Přesně tenhle vzor (vyber v selectu → načti
detail) budeš potřebovat pro appku typu "vyber město, zobraz počasí".

## Požadavky

- Napiš komponentu `UserDetail`.
- Vykresli `<select>` s pevně danými možnostmi — ID uživatelů `1` až `5`
  (žádný fetch na naplnění selectu není potřeba, jen napevno v kódu).
- Když se vybrané ID změní, načti detail uživatele z
  `https://jsonplaceholder.typicode.com/users/{id}` (`useEffect` se
  závislostí na vybraném ID).
- Tři stavy jako v `01-seznam-uzivatelu`: `Načítám...`, `Chyba: {zpráva}`,
  zobrazený detail.
- Po úspěšném načtení zobraz `name`, `email` a `company.name`.
- **Ošetři zastaralou odpověď** (viz `THEORY.md`) — teď už se závislost
  fakt mění (uživatel může select rychle přepínat), takže tahle past je
  reálná, ne jen teoretická.

### Příklady výběru → vykreslený obsah

| Vybrané ID | Vykreslený obsah                                                        |
|------------|-----------------------------------------------------------------------------|
| `1`        | `Leanne Graham` / `Sincere@april.biz` / `Romaguera-Crona`                  |
| `2`        | `Ervin Howell` / `Shanna@melissa.tv` / `Deckow-Crist`                      |
| `3`        | `Clementine Bauch` / `Nathan@yesenia.net` / `Romaguera-Jacobson`           |

## Bonus

- Přidej cache — jakmile appka detail uživatele jednou načte, při
  opětovném výběru stejného ID už fetch neopakuj (použij např. objekt/`Map`
  v `useState`, kde si podle ID pamatuješ už načtené detaily).

# 01 — Seznam uživatelů

První `useEffect` — načtení dat z reálného API při vykreslení komponenty.

## Požadavky

- Napiš komponentu `UserList`, která při vykreslení (`useEffect` s prázdným dependency polem) načte uživatele z
  `https://jsonplaceholder.typicode.com/users` (veřejné testovací API, žádný klíč není potřeba).
- Drž si tři stavy: `users` (pole, zpočátku `[]`), `loading` (zpočátku
  `true`), `error` (zpočátku `null`).
- Dokud se načítá, zobraz `Načítám...`.
- Pokud fetch selže (`.catch`), zobraz `Chyba: {zpráva}`.
- Po úspěšném načtení zobraz seznam jmen uživatelů (`.map()` + `key`, viz
  `02-podmineny-render-a-seznamy`).
- V `App` vykresli `UserList`.

### Příklady stavů → vykreslený obsah

| Stav                                     | Vykreslený obsah                            |
|------------------------------------------|---------------------------------------------|
| právě se načítá                          | `Načítám...`                                |
| fetch selhal (např. vypnutý internet)    | `Chyba: ...` (konkrétní zpráva podle chyby) |
| úspěšně načteno (API vrací 10 uživatelů) | seznam 10 jmen                              |

## Bonus

- Přidej tlačítko `Znovu načíst`, které zopakuje fetch (bez reloadu celé stránky). Fetch logiku vytáhni do samostatné
  funkce, kterou zavolá jak
  `useEffect` při mountu, tak handler tlačítka — ať kód není duplicitně na dvou místech.
- Po kliknutí na `Znovu načíst` se má appka znovu na chvíli dostat do stavu `Načítám...`.

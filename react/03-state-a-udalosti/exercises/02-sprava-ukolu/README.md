# 02 — Správa úkolů

Těžší cvičení — spoj `useState`, controlled input a všechno z
`02-podmineny-render-a-seznamy` (`.map()`, `key`, podmíněný render) do
jedné interaktivní komponenty. Přidávání a mazání úkolů, ne jen jejich
zobrazení.

## Požadavky

- Napiš typ `Task` (`id: string`, `title: string`, `done: boolean`).
- Napiš komponentu `TaskManager`, která si přes `useState` drží pole
  `tasks: Task[]` (počáteční hodnota `[]`).
- Přidej controlled text input a tlačítko `Přidat`:
  - po kliknutí přidá do seznamu nový úkol s `title` z inputu (`done: false`,
    vygeneruj unikátní `id`, např. `crypto.randomUUID()`)
  - po přidání se input vyprázdní
  - použij immutabilní update (viz `THEORY.md` — `03-state-a-udalosti`),
    ne mutaci pole
- Ke každému úkolu přidej tlačítko `Hotovo`/`Vrátit`, kterým přepneš jeho
  `done` (bez mutace objektu úkolu).
- Ke každému úkolu přidej tlačítko `Smazat`, kterým ho ze seznamu odstraníš.
- Hotový úkol vykresli jinak než nehotový (viz `02-podmineny-render-a-seznamy`).
- Pokud je seznam prázdný, zobraz `Žádné úkoly.`.
- V `App` vykresli `TaskManager`.

### Příklady akcí → zobrazený seznam

| Akce (v pořadí)                                                  | Zobrazený seznam           |
|--------------------------------------------------------------------|-------------------------------|
| (start)                                                             | `Žádné úkoly.`               |
| napiš "Nakoupit", klik `Přidat`                                     | `Nakoupit`                   |
| napiš "Uklidit", klik `Přidat`                                      | `Nakoupit` / `Uklidit`        |
| klik `Hotovo` u "Nakoupit"                                          | `✓ Nakoupit` / `Uklidit`      |
| klik `Smazat` u "Uklidit"                                           | `✓ Nakoupit`                 |
| klik `Smazat` u "Nakoupit"                                          | `Žádné úkoly.`                |

## Bonus

- Tlačítko `Přidat` (a totéž pro klávesu Enter v inputu, pokud ji řešíš)
  nesmí přidat úkol, jehož název je po `trim()` prázdný řetězec.
- Název úkolu se navíc uloží už oříznutý (`trim()`), ne s mezerami navíc.

### Příklady akcí → zobrazený seznam (bonus)

| Akce (v pořadí)                                  | Zobrazený seznam |
|-----------------------------------------------------|---------------------|
| input necháš prázdný, klik `Přidat`                  | `Žádné úkoly.`      |
| napiš jen mezery `"   "`, klik `Přidat`              | `Žádné úkoly.`      |
| napiš `"  Nakoupit  "`, klik `Přidat`                | `Nakoupit`          |

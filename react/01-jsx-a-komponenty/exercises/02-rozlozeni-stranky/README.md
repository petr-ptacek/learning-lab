# 02 — Rozložení stránky

Procvič si `children` a pojmenované "sloty" (props typu `React.ReactNode`)
na složitější komponentě, než byla vizitka.

## Požadavky

- Napiš function komponentu `PageLayout` s props:
  - `header: React.ReactNode` — obsah hlavičky
  - `footer: React.ReactNode` — obsah patičky
  - `children: React.ReactNode` — hlavní obsah stránky (výchozí "slot")
- `PageLayout` vykreslí části v pořadí **header → children → footer**
  (obal kolem jednotlivých částí, např. `<header>`/`<main>`/`<footer>`,
  je na tobě).
- V `App` použij `PageLayout` a naplň všechny tři props libovolným JSX
  obsahem (nadpisy, odstavce, ...).

### Příklady props → pořadí ve vykresleném obsahu

| header                | children                                    | footer                             | Pořadí ve výstupu                                  |
|-----------------------|----------------------------------------------|-------------------------------------|-----------------------------------------------------|
| `<h1>Blog</h1>`       | `<p>Vítej na blogu!</p>`                     | `<small>&copy; 2026</small>`       | `Blog` / `Vítej na blogu!` / `© 2026`               |
| `<nav>Menu</nav>`     | `<><p>Odstavec 1</p><p>Odstavec 2</p></>`    | `<p>Kontakt: info@example.com</p>` | `Menu` / `Odstavec 1` / `Odstavec 2` / `Kontakt: info@example.com` |
| `<span>Header</span>` | `"Prostý text bez tagu"`                     | `<p>Konec</p>`                     | `Header` / `Prostý text bez tagu` / `Konec`         |

Třetí příklad není překlep — `React.ReactNode` klidně přijme i obyčejný
text bez obalujícího JSX tagu.

## Bonus

- Napiš komponentu `Alert`, která kombinuje pojmenovaný prop **a**
  `children` zároveň:
  - `icon: React.ReactNode` — ikona/značka na začátku
  - `children: React.ReactNode` — text zprávy
- V `App` vlož `Alert` dovnitř hlavního obsahu `PageLayout`.

### Příklady props → vykreslený obsah (bonus)

| icon      | children                     | Vykreslený obsah              |
|-----------|-------------------------------|--------------------------------|
| `⚠️`      | `Tohle je varování.`         | `⚠️ Tohle je varování.`       |
| `✅`      | `Uloženo.`                    | `✅ Uloženo.`                  |

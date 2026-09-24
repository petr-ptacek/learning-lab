# react

Specifika tohoto tématu:

- Pracujeme s aktuální stabilní verzí React (19) — pouze function komponenty
  a hooky, žádné class komponenty (v moderním Reactu se nepoužívají).
- Čistý JavaScript (`.jsx`), bez TypeScriptu — ať je pozornost na Reactu
  samotném, ne na typovém systému.
- Každé cvičení je samostatný Vite projekt s vlastním `package.json` —
  stejně izolované jako cvičení v Pythonu (žádný sdílený "app shell" mezi
  cvičeními, to by si vynucovalo router dřív, než ho probereme, viz
  10-routing v [`ROADMAP.md`](ROADMAP.md)).
- Scaffold cvičení (`solution/`, po dořešení i `reference/`) obsahuje jen
  to nutné ke spuštění — žádný linter, žádné demo assety. `src/App.jsx` je
  prázdný stub, kam se píše řešení; `main.jsx`, `index.html`,
  `vite.config.js`, `package.json` jsou předpřipravené a funkční.
- Spuštění cvičení: `npm install && npm run dev` uvnitř `solution/`
  (resp. `reference/`), pak otevřít URL, kterou Vite vypíše.
- Bonus (pokud zadání má sekci `## Bonus`) nejde do `main.jsx`/`App.jsx`,
  ale do sesterské dvojice souborů `src/AppBonus.jsx` + `src/main-bonus.jsx`
  a vlastního `bonus.html` (Vite bez dalšího configu servíruje víc HTML
  vstupních bodů zároveň) — spustí se stejným `npm run dev`, jen se otevře
  `/bonus.html` místo `/index.html`.
- Uživatel (Petr) je zkušený Vue.js developer, React se učí od základů —
  React koncepty klidně kontrastuj s Vue tam, kde to pomůže pochopení
  (JSX vs. template, props, reaktivita, ...), ale nepředpokládej znalost
  Reactu samotného.
- Odkaz zpět na kořenový [`CLAUDE.md`](../CLAUDE.md) pro obecná pravidla
  repa.

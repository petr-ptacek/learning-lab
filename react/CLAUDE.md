# react

Specifika tohoto tématu:

- Pracujeme s aktuální stabilní verzí React (19) — pouze function komponenty
  a hooky, žádné class komponenty (v moderním Reactu se nepoužívají).
- TypeScript (`.tsx`) — props, návratové hodnoty i state jsou typované.
  Typy piš explicitně tam, kde to má smysl pro čitelnost (např. `interface`/
  `type` pro props), ale nezabředávej do pokročilých TS technik, pokud to
  koncept z `ROADMAPU.md` zrovna neřeší — těžiště je na Reactu, ne na TS.
- Každé cvičení je samostatný Vite projekt s vlastním `package.json` —
  stejně izolované jako cvičení v Pythonu (žádný sdílený "app shell" mezi
  cvičeními, to by si vynucovalo router dřív, než ho probereme, viz
  10-routing v [`ROADMAP.md`](ROADMAP.md)).
- Scaffold cvičení (`solution/`, po dořešení i `reference/`) obsahuje jen
  to nutné ke spuštění — žádný linter, žádné demo assety. `src/App.tsx` je
  prázdný stub, kam se píše řešení; `main.tsx`, `index.html`,
  `vite.config.ts`, `tsconfig*.json`, `package.json` jsou předpřipravené
  a funkční.
- Spuštění cvičení: `npm install && npm run dev` uvnitř `solution/`
  (resp. `reference/`), pak otevřít URL, kterou Vite vypíše. `npm run build`
  navíc přes `tsc -b` zkontroluje typy.
- Bonus (pokud zadání má sekci `## Bonus`) jde přes **jediný entry point**
  (`index.html` → `src/main.tsx` → `src/App.tsx`) — žádný další
  `bonus.html` ani `main-bonus.tsx`. Bonus se píše do sesterské komponenty
  `src/AppBonus.tsx` (prázdný stub), kterou `App.tsx` vyrenderuje pod
  základním řešením, takže je obojí vidět na jedné stránce po `npm run dev`.
- Uživatel (Petr) je zkušený Vue.js developer (senior), React se učí od
  základů — nepředpokládej znalost Reactu samotného, ale Vue znalost ano.
  V `THEORY.md` u konceptů, kde existuje přímá obdoba ve Vue (komponenty,
  props, children/sloty, reaktivita/state, lifecycle/efekty, ...), ukazuj
  **konkrétní kód vedle sebe** — krátký Vue úryvek (SFC/`<script setup>`)
  a jeho React ekvivalent, ne jen slovní zmínku "jako ve Vue". Cílem je
  využít existující mentální model, ne ho jen připomenout.
- Odkaz zpět na kořenový [`CLAUDE.md`](../CLAUDE.md) pro obecná pravidla
  repa.

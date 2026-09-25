# 01 — Seznam úkolů

Procvič si `.map()`, `key` a podmíněné renderování na jednoduchém seznamu.

## Požadavky

- Napiš typ/interface `Task` s poli `id: string`, `title: string`,
  `done: boolean`.
- Napiš komponentu `TaskList` s props `tasks: Task[]`.
- Pro každý úkol vykresli `<li>` s `title`. Hotový úkol (`done: true`)
  vykresli jinak než nehotový — např. přeškrtnutý (`<s>{title}</s>`) nebo
  s prefixem `✓ `.
- Pokud je `tasks` prázdné pole, místo seznamu zobraz text `Žádné úkoly.`.
- V `App` vytvoř pole úkolů napevno (žádný vstup od uživatele — to přijde
  až s `useState` v `03-state-a-udalosti`) a vykresli `TaskList`.

### Příklady props → vykreslený obsah

| tasks                                                                 | Vykreslený obsah                          |
|------------------------------------------------------------------------|--------------------------------------------|
| `[{id:'1',title:'Nakoupit',done:false},{id:'2',title:'Uklidit',done:true}]` | `Nakoupit` / `✓ Uklidit` (přeškrtnuté) |
| `[{id:'1',title:'Zaplatit účty',done:false}]`                          | `Zaplatit účty`                           |
| `[]`                                                                    | `Žádné úkoly.`                            |

## Bonus

- Pokud jsou v neprázdném seznamu hotové **úplně všechny** úkoly, zobraz
  nad seznamem navíc hlášku `🎉 Vše hotovo!`.

### Příklady props → vykreslený obsah (bonus)

| tasks                                                                       | Vykreslený obsah                                  |
|--------------------------------------------------------------------------------|-----------------------------------------------------|
| `[{id:'1',title:'Nakoupit',done:true},{id:'2',title:'Uklidit',done:true}]`      | `🎉 Vše hotovo!` / `✓ Nakoupit` / `✓ Uklidit`       |
| `[{id:'1',title:'Nakoupit',done:true},{id:'2',title:'Uklidit',done:false}]`     | `✓ Nakoupit` / `Uklidit` (bez hlášky)              |
| `[]`                                                                            | `Žádné úkoly.` (bez hlášky, i kdyby "všechny" `[].every()` vracelo `true`) |

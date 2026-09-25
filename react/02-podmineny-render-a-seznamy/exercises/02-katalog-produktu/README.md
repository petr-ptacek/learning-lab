# 02 — Katalog produktů

Těžší cvičení na `.map()` a podmíněné renderování — tentokrát vnořené (seznam v seznamu) a na dvou úrovních zároveň.

## Požadavky

- Napiš typy `Product` (`id: string`, `name: string`, `inStock: boolean`)
  a `Category` (`id: string`, `name: string`, `products: Product[]`).
- Napiš komponentu `CatalogList` s props `categories: Category[]`.
- Pro každou kategorii vykresli nadpis (`<h2>{category.name}</h2>`) a pod ním seznam jejích produktů.
- Produkt, který není skladem (`inStock: false`), vykresli jinak než skladem — např. přeškrtnutý nebo s dovětkem
  ` (vyprodáno)`.
- Pokud kategorie nemá žádné produkty, místo seznamu zobraz
  `Žádné produkty v této kategorii.`.
- Pokud je celé pole `categories` prázdné, zobraz jen `Žádné kategorie.`
  (a nic jiného).
- V `App` vytvoř pole kategorií napevno a vykresli `CatalogList`.

### Příklady props → vykreslený obsah

| categories                                                                                                       | Vykreslený obsah                                                    |
|------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `[{id:'1',name:'Nápoje',products:[{id:'p1',name:'Voda',inStock:true},{id:'p2',name:'Limonáda',inStock:false}]}]` | `Nápoje` / `Voda` / `Limonáda (vyprodáno)`                          |
| `[{id:'1',name:'Nápoje',products:[]},{id:'2',name:'Pečivo',products:[{id:'p3',name:'Chleba',inStock:true}]}]`    | `Nápoje` / `Žádné produkty v této kategorii.` / `Pečivo` / `Chleba` |
| `[]`                                                                                                             | `Žádné kategorie.`                                                  |

## Bonus

- Nad seznam kategorií přidej přehled — pro každou kategorii jeden řádek
  `<dt>{category.name}</dt><dd>{počet produktů} produktů</dd>` v jednom
  `<dl>`. Protože z jedné položky `.map()` vracíš dva sourozední elementy najednou, budeš potřebovat
  `<Fragment key={...}>` (zkrácený zápis
  `<>...</>` `key` nepřijme — viz `THEORY.md`).
- Přehled se zobrazí, jen když `categories` není prázdné pole.

### Příklady props → vykreslený obsah (bonus)

| categories                                                                                                       | Přehled (`<dl>`)                        |
|------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| `[{id:'1',name:'Nápoje',products:[{id:'p1',name:'Voda',inStock:true},{id:'p2',name:'Limonáda',inStock:false}]}]` | `Nápoje` / `2 produktů`                 |
| `[{id:'1',name:'Nápoje',products:[]}]`                                                                           | `Nápoje` / `0 produktů`                 |
| `[]`                                                                                                             | (žádný přehled, jen `Žádné kategorie.`) |

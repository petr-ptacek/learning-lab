# 01 — JSX a komponenty

## Cíl

Naučit se základní stavební blok Reactu — komponentu: co je JSX, jak napsat
function komponentu, jak jí předat data přes props a jak komponenty skládat
dohromady (kompozice). Všechno další (state, efekty, ...) na tomhle staví.

## Jak spustit cvičení

Uvnitř `solution/` (resp. `reference/`) daného cvičení:

```
npm install
npm run dev
```

Vite vypíše URL (typicky `http://localhost:5173`), na které appka běží.
Změny v kódu se promítnou automaticky (hot reload).

## JSX

JSX je syntaktické rozšíření JavaScriptu, které vypadá jako HTML, ale je to
pořád JavaScript — pod kapotou se kompiluje na volání funkcí, které vytvoří
strom objektů popisujících UI (podobně jako Vue template kompiluje na
render funkce, jen tady je ta podobnost s JS syntaxí vidět přímo).

```jsx
const element = <h1>Ahoj, světe!</h1>
```

Rozdíly oproti HTML:

- `className` místo `class` (`class` je v JS rezervované slovo)
- atributy v `camelCase` (`onClick`, `tabIndex`, ...)
- všechny tagy musí být uzavřené, i ty bez obsahu (`<img />`, ne `<img>`)
- JSX výraz musí mít **jeden root element** — víc elementů vedle sebe se
  zabalí do `<div>...</div>` nebo do fragmentu `<>...</>` (fragment nic
  nepřidá do výsledného DOM)

## JavaScript uvnitř JSX

Uvnitř `{}` můžeš do JSX vložit libovolný JS **výraz** (ne příkaz — takže
ne `if`, `for`; na podmíněné renderování a seznamy dojde v příštím
konceptu).

```jsx
const name = 'Petr'
const element = <p>Ahoj, {name}! Dnes je {new Date().toLocaleDateString()}.</p>
```

## Function komponenty

Komponenta je obyčejná JS funkce, která vrací JSX. Jméno komponenty musí
začínat velkým písmenem (`PascalCase`) — tím React pozná komponentu od
obyčejného HTML tagu (`<Profile />` vs. `<profile />`).

```jsx
function Greeting() {
  return <h1>Ahoj!</h1>
}
```

Použití komponenty vypadá jako vlastní HTML tag:

```jsx
function App() {
  return <Greeting />
}
```

## Props

Props jsou vstupní data komponenty — předávají se jako atributy, uvnitř
komponenty je dostaneš jako jeden objekt (argument funkce), typicky rovnou
destrukturovaný. Props jsou **read-only** — komponenta je nesmí měnit.

```jsx
function Greeting({ name }) {
  return <h1>Ahoj, {name}!</h1>
}

function App() {
  return <Greeting name="Petr" />
}
```

Ve Vue je to koncepčně to samé (`defineProps`), jen bez automatické
validace typů — pokud chceš validaci props, musí to být TypeScript nebo
knihovna navíc (např. `prop-types`). V tomhle repu props zatím necháváme
bez validace.

## Children a kompozice

Obsah mezi otevíracím a zavíracím tagem komponenty je dostupný uvnitř jako
speciální prop `children`:

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>
}

function App() {
  return (
    <Card>
      <p>Tohle je obsah karty.</p>
    </Card>
  )
}
```

To je obdoba Vue slotů (`<slot />`). React nemá dědičnost komponent — místo
toho se preferuje **kompozice**: skládání menších komponent do větších,
podobně jako v Reactu chybí koncept "extends komponenty" a řeší se to
vnořováním a `children` (nebo props, které jsou samy JSX).

## Klíčové pojmy

- JSX — syntax rozšíření JS, kompiluje se na volání funkcí vytvářejících
  popis UI
- function komponenta — funkce v `PascalCase`, vrací JSX
- props — vstupní, read-only data komponenty
- `children` — speciální prop pro obsah mezi tagy komponenty
- kompozice — skládání komponent vnořováním místo dědičnosti

# 01 — JSX a komponenty

## Cíl

Naučit se základní stavební blok Reactu — komponentu: co je JSX, jak napsat function komponentu, jak jí předat data přes
props a jak komponenty skládat dohromady (kompozice). Všechno další (state, efekty, ...) na tomhle staví.

## Jak spustit cvičení

Uvnitř `solution/` (resp. `reference/`) daného cvičení:

```
npm install
npm run dev
```

Vite vypíše URL (typicky `http://localhost:5173`), na které appka běží. Změny v kódu se promítnou automaticky (hot
reload).

## JSX

JSX je syntaktické rozšíření JavaScriptu, které vypadá jako HTML, ale je to
pořád JavaScript — pod kapotou se kompiluje na volání funkcí, které vytvoří
strom objektů popisujících UI. Vue template dělá koncepčně to samé (taky se
kompiluje na render funkce) — rozdíl je, že JSX tuhle podobnost s JS
syntaxí nechává vidět přímo, zatímco Vue template je vlastní, oddělený
jazyk (proto `v-if`, `v-for`, `{{ }}` místo obyčejného JS):

```vue
<!-- Vue -->
<template>
  <h1>Ahoj, světe!</h1>
</template>
```

```tsx
// React
const element = <h1>Ahoj, světe!</h1>
```

Rozdíly oproti HTML:

- `className` místo `class` (`class` je v JS rezervované slovo)
- atributy v `camelCase` (`onClick`, `tabIndex`, ...)
- všechny tagy musí být uzavřené, i ty bez obsahu (`<img />`, ne `<img>`)
- JSX výraz musí mít **jeden root element** — víc elementů vedle sebe se zabalí do `<div>...</div>` nebo do fragmentu
  `<>...</>` (fragment nic nepřidá do výsledného DOM)

## JavaScript uvnitř JSX

Uvnitř `{}` můžeš do JSX vložit libovolný JS **výraz** (ne příkaz — takže ne `if`, `for`; na podmíněné renderování a
seznamy dojde v příštím konceptu).

```tsx
const name = 'Petr'
const element = <p>Ahoj, { name }! Dnes je { new Date().toLocaleDateString() }.</p>
```

## Function komponenty

Komponenta je obyčejná JS funkce, která vrací JSX. Jméno komponenty musí začínat velkým písmenem (`PascalCase`) — tím
React pozná komponentu od obyčejného HTML tagu (`<Profile />` vs. `<profile />`).

Ve Vue je komponenta soubor (`.vue` SFC), tady je to funkce ve stejném
`.tsx` souboru — klidně jich může být v jednom souboru víc, dokud jde o
malé, úzce související komponenty (žádné pravidlo "1 komponenta = 1 soubor"
jako u Vue SFC).

```vue
<!-- Vue: Greeting.vue -->
<template>
  <h1>Ahoj!</h1>
</template>
```

```tsx
// React
function Greeting() {
  return <h1>Ahoj!</h1>
}
```

Použití komponenty vypadá jako vlastní HTML tag — stejně jako ve Vue
(automaticky, nebo přes `components: { Greeting }` u Options API):

```tsx
function App() {
  return <Greeting />
}
```

## Props

Props jsou vstupní data komponenty — předávají se jako atributy, uvnitř komponenty je dostaneš jako jeden objekt
(argument funkce), typicky rovnou destrukturovaný. Props jsou **read-only** — komponenta je nesmí měnit.

Typ props se popíše přes `interface` (nebo `type`) a napíše se za destrukturovaný parametr — koncepčně přesně to samé
jako typované `defineProps<Props>()` ve Vue `<script setup>`, jen bez speciální syntaxe navíc (je to obyčejný TS typ
parametru funkce):

```vue
<!-- Vue: Greeting.vue -->
<script setup lang="ts">
interface Props {
  name: string
}

const { name } = defineProps<Props>()
</script>

<template>
  <h1>Ahoj, {{ name }}!</h1>
</template>
```

```tsx
// React
interface GreetingProps {
  name: string
}

function Greeting({ name }: GreetingProps) {
  return <h1>Ahoj, { name }!</h1>
}

function App() {
  return <Greeting name="Petr" />
}
```

## Children a kompozice

Obsah mezi otevíracím a zavíracím tagem komponenty je dostupný uvnitř jako speciální prop `children`, typovaný jako
`React.ReactNode` (cokoliv, co React umí vykreslit — JSX, string, číslo, pole těchto věcí, ...). Je to přímá obdoba
Vue defaultního slotu (`<slot />`) — jen ve Vue je slot deklarovaný v template, v Reactu je `children` obyčejný prop:

```vue
<!-- Vue: Card.vue -->
<template>
  <div class="card">
    <slot />
  </div>
</template>

<!-- použití -->
<Card>
  <p>Tohle je obsah karty.</p>
</Card>
```

```tsx
// React
interface CardProps {
  children: React.ReactNode
}

function Card({ children }: CardProps) {
  return <div className="card">{ children }</div>
}

function App() {
  return (
    <Card>
      <p>Tohle je obsah karty.</p>
    </Card>
  )
}
```

`children` je rezervované jméno propu ve dvou konkrétních věcech:

- **automatické plnění** — cokoliv napíšeš mezi `<Tag>...</Tag>`, JSX transformace automaticky předá jako
  `props.children`, aniž bys psal `children={...}` explicitně; přejmenovat to nejde
- pokud `children` v typu props nemáš deklarovaný, TypeScript ti nedovolí do komponenty nic vnořit — je to jediné
  jméno propu, které JSX/TS takhle speciálně zachytává

Co rezervované **není**, je typ. `React.ReactNode` je jen konvenční výchozí volba (obvykle chceš přijmout "cokoliv
renderovatelného"), ne vynucený typ — klidně ho zúžíš, přesně jako u kteréhokoli jiného propu:

```tsx
interface CounterProps {
  children: number
}

function Counter({ children }: CounterProps) {
  return <div>Count: {children}</div>
}

// <Counter>{42}</Counter>          — OK
// <Counter>not a number</Counter>  — chyba: typ 'children' je 'number', ne 'string'
```

Jméno a mechanismus plnění = rezervované/speciální (1:1 obdoba Vue defaultního slotu). Typ = obyčejný TS typ jako
u jakéhokoli jiného propu.

React nemá dědičnost komponent — místo toho se preferuje **kompozice**: skládání menších komponent do větších, stejně
jako ve Vue neexistuje "extends komponenty" a řeší se to vnořováním a sloty (nebo v Reactu `children`/props, které jsou
samy JSX).

Pojmenované Vue sloty (`<slot name="...">`) nemají v Reactu speciální syntax — použije se prostě další pojmenovaný
prop typu `React.ReactNode` (`children` je tak trochu "výchozí slot", jen zabudovaný do jazyka):

```vue
<!-- Vue: Card.vue -->
<template>
  <div class="card">
    <header><slot name="header" /></header>
    <div class="body"><slot /></div>
  </div>
</template>

<!-- použití -->
<Card>
  <template #header>
    <h2>Nadpis</h2>
  </template>
  <p>Obsah karty</p>
</Card>
```

```tsx
// React
interface CardProps {
  header: React.ReactNode
  children: React.ReactNode
}

function Card({ header, children }: CardProps) {
  return (
    <div className="card">
      <header>{header}</header>
      <div className="body">{children}</div>
    </div>
  )
}

function App() {
  return (
    <Card header={<h2>Nadpis</h2>}>
      <p>Obsah karty</p>
    </Card>
  )
}
```

## Klíčové pojmy

- JSX — syntax rozšíření JS, kompiluje se na volání funkcí vytvářejících popis UI
- function komponenta — funkce v `PascalCase`, vrací JSX
- props — vstupní, read-only data komponenty, typovaná přes `interface`/`type`
- `children` — speciální prop pro obsah mezi tagy komponenty, typ `React.ReactNode`
- kompozice — skládání komponent vnořováním místo dědičnosti

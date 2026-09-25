# 02 — Podmíněný render a seznamy

## Cíl

Naučit se vykreslovat UI, které se mění podle dat: podmíněně (zobraz/skryj podle nějaké podmínky) a opakovaně (vykresli
seznam položek). Staví na
`01-jsx-a-komponenty` — pořád jsou to jen funkce vracející JSX, teď se do JSX vejde i logika.

## Jak spustit cvičení

Stejně jako u předchozího konceptu — uvnitř `solution/` (resp.
`reference/`) daného cvičení:

```
npm install
npm run dev
```

## Podmíněné renderování

Ve Vue máš na podmíněné renderování direktivy (`v-if`/`v-else-if`/`v-else`,
`v-show`). V Reactu žádné direktivy nejsou — je to pořád obyčejný JavaScript, jen použitý uvnitř JSX.

**Ternární operátor** (když potřebuješ vybrat mezi dvěma variantami):

```vue
<!-- Vue -->
<template>
  <p v-if="isLoggedIn">Vítej zpět!</p>
  <p v-else>Přihlaš se.</p>
</template>
```

```tsx
// React
function Greeting({ isLoggedIn }: { isLoggedIn: boolean }) {
  return <p>{ isLoggedIn ? 'Vítej zpět!' : 'Přihlaš se.' }</p>
}
```

**`&&` operátor** (když chceš něco zobrazit, nebo nic — obdoba `v-if` bez
`v-else` větve):

```vue
<!-- Vue -->
<template>
  <span v-if="unreadCount > 0">{{ unreadCount }} nových zpráv</span>
</template>
```

```tsx
// React
function Badge({ unreadCount }: { unreadCount: number }) {
  return <>{ unreadCount > 0 && <span>{ unreadCount } nových zpráv</span> }</>
}
```

⚠️ Pozor na `&&` s číslem na levé straně: `{count && <p>...</p>}` s
`count === 0` vykreslí do stránky `0` (protože `0` je "falsy", ale JSX ho pořád vykreslí jako text). Řešení:
`{count > 0 && <p>...</p>}` — porovnání vrací `boolean`, ne `number`.

**Early return** (když je celá komponenta jinak úplně jiná, ne jen jeden kousek JSX — obdoba `v-if` na celém root
elementu):

```tsx
function UserProfile({ user }: { user: User | null }) {
  if ( !user ) {
    return <p>Uživatel nenalezen.</p>
  }

  return <h1>{ user.name }</h1>
}
```

Vue nemá pro tenhle případ přímou obdobu (`v-if` na kořenovém elementu funguje jinak) — v Reactu je to jen normální `if`
s `return`, protože komponenta je normální funkce.

`v-show` (přepínání `display` v CSS, element zůstává v DOM) nemá v Reactu vestavěnou obdobu — pokud to potřebuješ, řešíš
to sám přes `style={{ display: ... }}`.

## Seznamy a `.map()`

Vue `v-for` má v Reactu obdobu v `.map()` — obyčejné pole se transformuje na pole JSX elementů:

```vue
<!-- Vue -->
<template>
  <ul>
    <li v-for="user in users" :key="user.id">{{ user.name }}</li>
  </ul>
</template>
```

```tsx
// React
function UserList({ users }: { users: User[] }) {
  return (
    <ul>
      { users.map((user) => (
        <li key={ user.id }>{ user.name }</li>
      )) }
    </ul>
  )
}
```

## `key`

`key` slouží Reactu (stejně jako `:key` Vue) k tomu, aby při překreslení poznal, která položka seznamu je která — i po
přidání/odebrání/přeřazení. Bez toho by React (i Vue) mohl omylem přepoužít DOM element pro jinou položku, než patří.

Pravidla:

- `key` musí být **stabilní** (stejná položka = stejný `key` napříč překreslením) a **unikátní** mezi sourozenci (ne
  nutně globálně)
- ideální `key` je nějaké skutečné ID dat (`user.id`), ne vygenerovaná hodnota (`Math.random()` už vůbec ne — to je jiný
  `key` při každém renderu)
- **index pole jako `key`** (`users.map((user, i) => <li key={i}>`) je poslední záchrana, jen když položky nemají žádné
  ID a seznam se nikdy nepřeskupuje/nefiltruje/nemaže z prostředka — jinak to vede k záhadným bugům (špatná položka si
  "podrží" state jiné položky)
- `key` se předává jen tomu nejvzdálenějšímu elementu z `.map()`, ne něčemu uvnitř

## Fragmenty v seznamu

Pokud `.map()` potřebuje vrátit víc než jeden element a chceš mu dát `key`, zkrácený zápis `<>...</>` `key` nepřijme —
musíš použít plný `<Fragment key={...}>`:

```tsx
import { Fragment } from 'react'

function Glossary({ items }: { items: { term: string; definition: string }[] }) {
  return (
    <dl>
      { items.map((item) => (
        <Fragment key={ item.term }>
          <dt>{ item.term }</dt>
          <dd>{ item.definition }</dd>
        </Fragment>
      )) }
    </dl>
  )
}
```

## Klíčové pojmy

- podmíněné renderování — ternární operátor (`? :`), `&&`, nebo early
  `return` uvnitř komponenty; žádné direktivy jako ve Vue
- `.map()` — transformace pole dat na pole JSX elementů, obdoba `v-for`
- `key` — stabilní, unikátní identifikátor položky seznamu; index pole jen jako poslední možnost
- `Fragment`/`<Fragment key={...}>` — když `.map()` vrací víc elementů a potřebuješ jim dát `key`

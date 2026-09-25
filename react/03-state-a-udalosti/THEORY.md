# 03 — State a události

## Cíl

Naučit se, jak komponenta drží vlastní data v čase (state) a jak reaguje na akce uživatele (události) — bez tohohle není
appka interaktivní, jen statické UI. Staví na `01-jsx-a-komponenty` a `02-podmineny-render-a-seznamy`
— komponenta se teď bude překreslovat znovu a znovu, pokaždé s aktuálním state.

## Jak spustit cvičení

Stejně jako u předchozích konceptů — uvnitř `solution/` (resp.
`reference/`) daného cvičení:

```
npm install
npm run dev
```

## Události

Ve Vue jsou event listenery direktiva (`@click="handler"`). V Reactu je to obyčejný prop v `camelCase`, kterému předáš
referenci na funkci:

```vue
<!-- Vue -->
<template>
  <button @click="handleClick">Klikni</button>
</template>
```

```tsx
// React
function App() {
  function handleClick() {
    console.log('kliknuto')
  }

  return <button onClick={ handleClick }>Klikni</button>
}
```

⚠️ `onClick={handleClick}` (reference na funkci), ne `onClick={handleClick()}`
(zavolání funkce hned při renderu, ne při kliknutí).

Když handleru potřebuješ předat argument, obalíš ho do šipkové funkce — Vue to řeší přímo v template
(`@click="handleClick(item.id)"`), v Reactu je `onClick` obyčejný JS výraz, takže žádná speciální syntax pro volání s
argumentem není:

```tsx
<button onClick={ () => handleClick(item.id) }>Smazat</button>
```

## `useState`

Vue má `ref()`/`reactive()` — proměnná je mutovatelná (`count.value++`) a framework si mutaci sám odchytí. React state
se **nikdy nemutuje** —
`useState` vrátí aktuální hodnotu a funkci na její *nahrazení*, která navíc řekne Reactu, že se má komponenta
překreslit:

```vue
<!-- Vue -->
<script setup>
  import { ref } from 'vue'

  const count = ref(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

```tsx
// React
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={ () => setCount(count + 1) }>{ count }</button>
}
```

**Funkcionální update** — když nová hodnota state závisí na té předchozí, je bezpečnější předat do setteru funkci místo
hodnoty (`setCount((c) => c + 1)`
místo `setCount(count + 1)`). Není to jen styl: `count` uvnitř handleru je hodnota z okamžiku, kdy se komponenta
naposledy vykreslila — pokud bys setter zavolal víckrát rychle po sobě se stejným zachyceným `count`, druhé volání by
"přepsalo" první. Funkcionální forma vždy dostane skutečně aktuální hodnotu.

## Controlled input (obdoba `v-model`)

Vue má na obousměrné svázání inputu se stavem `v-model`. React žádnou takovou zkratku nemá — vždycky to propojíš ručně
přes `value` + `onChange`:

```vue
<!-- Vue -->
<script setup>
  import { ref } from 'vue'

  const name = ref('')
</script>

<template>
  <input v-model="name" />
</template>
```

```tsx
// React
import { useState } from 'react'

function NameInput() {
  const [name, setName] = useState('')
  return <input value={ name } onChange={ (e) => setName(e.target.value) } />
}
```

Input, který má `value` navázanou na state, se nazývá **controlled** — jeho zobrazená hodnota je vždycky přesně to, co
je v state (React ji řídí), ne to, co si "pamatuje" sám prohlížeč.

## Immutabilita objektů a polí ve state

Pokud je state objekt nebo pole, nikdy ho nemutuj (`state.push(...)`,
`state.field = ...`) — React pozná změnu jen podle nové reference, takže mutace v místě se nikdy neprojeví (React si
"myslí", že se nic nezměnilo). Vždycky vytvoř novou hodnotu:

```tsx
// pole
setItems((items) => [...items, newItem])

// objekt
setUser((user) => ({ ...user, name: 'Petr' }))
```

## Klíčové pojmy

- event handler — prop v `camelCase` (`onClick`, `onChange`, ...), předává se reference na funkci, ne její zavolání
- `useState` — hook pro lokální state komponenty, vrací `[hodnota, setHodnota]`
- funkcionální update — `setHodnota((prev) => ...)`, když nová hodnota závisí na předchozí
- controlled input — `value` + `onChange`, ruční obdoba `v-model`
- immutabilita — state (obzvlášť objekty/pole) se nikdy nemutuje, vždy se vytváří nová hodnota

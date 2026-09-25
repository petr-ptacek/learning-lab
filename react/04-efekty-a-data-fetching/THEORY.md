# 04 — Efekty a data fetching

## Cíl

Naučit se reagovat na věci mimo čistý render — nejčastěji načítání dat
z API, ale obecně cokoliv, co komponenta dělá "navíc" k tomu, že vrací
JSX (tzv. side effect). Staví na `03-state-a-udalosti` (state pro
loading/data/error) a `02-podmineny-render-a-seznamy` (podmíněné
zobrazení těchto stavů).

## Jak spustit cvičení

Stejně jako u předchozích konceptů — uvnitř `solution/` (resp.
`reference/`) daného cvičení:

```
npm install
npm run dev
```

## `useEffect` základy

Vue rozděluje lifecycle do víc hooků (`onMounted`, `onUnmounted`, `watch`).
React to sjednocuje do jednoho `useEffect` — funkce, která se spustí **po**
vykreslení, a druhý argument (dependency pole) určuje, kdy se spustí znovu.

```vue
<!-- Vue -->
<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  console.log('komponenta je v DOM')
})
</script>
```

```tsx
// React
import { useEffect } from 'react'

useEffect(() => {
  console.log('komponenta je v DOM')
}, [])
```

Tři varianty dependency pole:

- **chybí úplně** → efekt běží po **každém** renderu (skoro nikdy nechceš)
- **`[]`** → efekt běží jen **jednou**, po prvním vykreslení (obdoba `onMounted`)
- **`[a, b]`** → efekt běží po prvním vykreslení a pak znovu pokaždé, když
  se změní `a` nebo `b` (obdoba `watch([a, b], ...)`)

## Cleanup funkce

Return z efektu je funkce, která se zavolá **před** dalším spuštěním
efektu a při odmountování komponenty — obdoba `onUnmounted`, ale svázaná
přímo s konkrétním efektem, ne deklarovaná zvlášť:

```vue
<!-- Vue -->
<script setup>
import { onMounted, onUnmounted } from 'vue'

let intervalId: number

onMounted(() => {
  intervalId = setInterval(tick, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>
```

```tsx
// React
useEffect(() => {
  const intervalId = setInterval(tick, 1000)
  return () => clearInterval(intervalId)
}, [])
```

## Fetch dat — tři stavy

Reálné načítání dat skoro vždy potřebuje tři stavy: **loading**, **error**,
**data**. Je to kombinace `useState` (`03-state-a-udalosti`), `useEffect`
a podmíněného renderování (`02-podmineny-render-a-seznamy`):

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)

    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then(setUser)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [userId])

  if (loading) return <p>Načítám...</p>
  if (error) return <p>Chyba: {error}</p>
  if (!user) return null

  return <h1>{user.name}</h1>
}
```

## Past: zastaralá odpověď (race condition)

Když se `userId` rychle změní (např. přepnutí v selectu), starší fetch
požadavek může dorazit **později** než novější a přepsat aktuální data
zastaralými. Řešení: `ignore` flag v cleanup funkci (nebo `AbortController`
pro skutečné zrušení requestu):

```tsx
useEffect(() => {
  let ignore = false

  fetch(`/api/users/${userId}`)
    .then((res) => res.json())
    .then((data) => {
      if (!ignore) setUser(data)
    })

  return () => {
    ignore = true
  }
}, [userId])
```

## `<StrictMode>` a dvojí spuštění efektů (dev mód)

`main.tsx` v každém cvičení obaluje appku do `<StrictMode>` — v **dev
módu** React kvůli odhalení chyb schválně zavolá mount → cleanup → mount
pro každý efekt. V síťové záložce tak uvidíš dvojnásobek requestů — to je
očekávané chování jen za vývoje (v produkčním buildu se to neděje), ne bug.
Je to další důvod, proč cleanup funkce nejsou volitelné.

## Pravidlo úplných závislostí

Do dependency pole patří všechny reaktivní hodnoty (props, state), které
efekt uvnitř používá. Vynechání závislosti vede k tomu, že efekt uvnitř
pracuje se "zamrzlou" hodnotou z renderu, kdy naposledy proběhl — ne s tou
aktuální.

## Klíčové pojmy

- `useEffect` — hook pro side effects, spouští se po vykreslení
- dependency pole — určuje, kdy se efekt spustí znovu (chybí = po každém
  renderu, `[]` = jen jednou, `[a, b]` = při změně `a`/`b`)
- cleanup funkce — `return` z efektu, volá se před dalším spuštěním
  a při odmountování
- race condition — starší fetch může dorazit později než novější, řeší
  `ignore` flag / `AbortController`
- `<StrictMode>` dvojí spuštění — v dev módu efekty běží
  mount→cleanup→mount, ne bug

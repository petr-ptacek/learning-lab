# Jak React skutečně funguje — mentální model pro Vue vývojáře

Tenhle dokument neučí novou syntax. Cílem je posunout mentální model —
proč se React chová jinak, než bys čekal z Vue, a proč se z toho rozdílu
rodí konkrétní třídy chyb (zamrzlé hodnoty, "zapomenutá" data, věci, co se
resetují, když by neměly).

## Vue: graf, který žije mezi rendery

Ve Vue `setup()` (nebo `<script setup>`) proběhne **jednou**. Vytvoří
graf reaktivity — `ref`, `reactive`, `computed`, `watch` — a ten graf pak
žije po celou dobu, co komponenta existuje. Vue sleduje, které části
šablony na kterých reaktivních hodnotách závisí, a při změně aktualizuje
jen ty konkrétní části DOM. Tvůj kód uvnitř `setup()` se znovu nespouští —
běží jen ty reaktivní "dráty", které jsi jednou zapojil.

```vue
<script setup>
import { ref, computed, watch } from 'vue'

const count = ref(0) // vytvořeno jednou
const doubled = computed(() => count.value * 2) // zapojeno jednou, pak žije samo

watch(count, (newCount) => {
  console.log('count je teď', newCount) // taky zapojeno jednou
})
</script>
```

`count`, `doubled` i ten `watch` handler existují **jednou** po celou dobu
života komponenty. Mění se jen hodnota uvnitř `count.value` — proměnná
`count` samotná je pořád ten samý objekt.

## React: funkce volaná znovu od nuly, pokaždé

React nemá žádný graf, který by žil mezi rendery. Komponenta je **funkce**
a React ji při každém renderu zavolá **celou znovu, od první řádky**.
Žádná proměnná deklarovaná uvnitř těla komponenty nepřežije do dalšího
renderu — vznikne znovu, s čerstvou hodnotou.

```tsx
function Counter() {
  const doubled = count * 2 // tohle se přepočítá úplně při KAŽDÉM renderu
  console.log('render Counteru') // uvidíš tenhle log při každém překreslení

  return <div>{doubled}</div>
}
```

To je ten fundamentální rozdíl: Vue si jednou postaví graf závislostí a pak
jen aktualizuje, co je potřeba. React nemá žádnou "paměť" mezi rendery —
pokaždé přepočítá úplně všechno v těle funkce, od začátku.

## Tak jak si React vůbec něco pamatuje?

Přesně tady vstupují hooky. `useState`, `useRef`, `useReducer` — to nejsou
proměnné v klasickém slova smyslu. Je to **půjčovna hodnot**: React si tu
hodnotu drží **mimo** tvou funkci, ve své vlastní interní paměti, svázanou
s konkrétní komponentou na konkrétním místě ve stromu. Při každém renderu
ti `useState` tu hodnotu jen **půjčí** zpátky.

```tsx
function Counter() {
  const [count, setCount] = useState(0)
  // `count` tady není proměnná, kterou by sis "pamatoval" mezi rendery —
  // je to snímek hodnoty, kterou React drží jinde, půjčený pro TENHLE render
}
```

Když zavoláš `setCount(1)`, neřekneš Reactu "změň tuhle proměnnou". Řekneš
mu "při příštím renderu mi půjč `1` místo toho, co bylo předtím" — a React
naplánuje nový render, kde se celá funkce zavolá znovu od začátku, tentokrát
s `count = 1`.

## Render je "fotka" — a closures ji drží

Tohle je zdroj většiny zmatků, o kterých píšeš. Každý render je vlastní
uzavření (closure) nad hodnotami z toho konkrétního momentu. Handler,
efekt nebo callback vytvořený v jednom renderu **vidí hodnoty z toho
renderu** — i když se mezitím komponenta znovu vykreslí s novými hodnotami.

```tsx
function Counter() {
  const [count, setCount] = useState(0)

  function handleClickLater() {
    setTimeout(() => {
      alert(`Count je ${count}`) // uvidí count z RENDERU, kdy vznikl handler
    }, 3000)
  }

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
      <button onClick={handleClickLater}>Za 3s ukaž count</button>
    </div>
  )
}
```

Klikni na "Za 3s ukaž count" a hned potom třikrát na "+1". Alert po 3
sekundách ukáže `0`, ne `3` — protože `handleClickLater` je closure z
renderu, kdy `count` bylo `0`. Ve Vue tenhle problém nemá obdobu, protože
`count.value` je pořád ten samý mutovatelný box, ne snímek.

Tohle je taky přesně důvod, proč u `useState` existuje **funkcionální
update** (`setCount((c) => c + 1)`) — React zaručí, že `c` je vždycky
aktuální hodnota v okamžiku zpracování, ne ta zamrzlá z closure.

## `useEffect` — closure, co běží mimo render

`useEffect` má stejný problém, jen víc viditelný, protože efekty typicky
žijí déle (intervaly, subscriby, fetch). Funkce, kterou předáš do
`useEffect`, je taky closure nad hodnotami z renderu, kdy ten konkrétní
běh efektu vznikl:

```tsx
function Counter() {
  const [count, setCount] = useState(0)

  useEffect(() => {
    const id = setInterval(() => {
      console.log(count) // ⚠️ vždycky vypíše 0 — closure z prvního renderu
    }, 1000)
    return () => clearInterval(id)
  }, []) // prázdné pole = efekt vznikl JEDNOU, natrvalo vidí count = 0

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
    </div>
  )
}
```

Tohle je klasika — "proč mi to v intervalu pořád ukazuje nulu, i když
`count` na obrazovce roste?". Efekt s `[]` vznikl přesně jednou, v prvním
renderu, a ta closure uvnitř `setInterval` je navždy uvězněná s `count`
rovným `0` z toho renderu. Komponenta se sice znovu renderuje (a nová
closure by viděla `count = 1`), ale ten `setInterval` z prvního běhu
efektu se svojí starou closure furt běží dál.

Řešení je právě to, co drží `THEORY.md` u `04-efekty-a-data-fetching` —
`count` patří do dependency pole. Pak React starý efekt (se starou
closure) uklidí přes cleanup funkci a založí nový, s čerstvou closure:

```tsx
useEffect(() => {
  const id = setInterval(() => {
    console.log(count) // teď vidí aktuální count z TOHOTO běhu efektu
  }, 1000)
  return () => clearInterval(id)
}, [count]) // efekt se přezakládá pokaždé, když se count změní
```

Ve Vue bys na stejnou věc použil `watchEffect`/`watch` a `count.value`
uvnitř by vždycky viděl aktuální hodnotu, protože je to pořád ten samý
mutovatelný ref — žádná closure z minulosti tam nekouká.

## Všechno v těle komponenty je nové, pokaždé

Ne jen primitivní hodnoty — **objekty, pole i funkce** deklarované v těle
komponenty jsou při každém renderu úplně nové (jiná reference), i když mají
stejný obsah:

```tsx
function List({ items }: { items: string[] }) {
  const config = { sortBy: 'name' } // NOVÝ objekt při každém renderu
  const handleClick = () => console.log('click') // NOVÁ funkce při každém renderu

  return <Child config={config} onClick={handleClick} />
}
```

`Child` tak při každém renderu `List`u dostane `config` i `onClick` jako
jinou referenci, i když "vypadají stejně". Pokud `Child` porovnává props
přes referenci (např. `React.memo`, nebo `useEffect` má `config`/`onClick`
v dependency poli), bude se to chovat, jako by se pokaždé změnilo —
protože technicky vzato se to fakt pokaždé změnilo. Vue tohle nepotká,
protože `reactive`/`ref` objekt je pořád ten samý box, jen se mění jeho
obsah.

Na tohle React nabízí protijed — `useMemo` (zapamatuje hodnotu) a
`useCallback` (zapamatuje funkci) mezi rendery, dokud se nezmění jejich
závislosti. K tomu se dostaneš v `09-vykon-a-memoizace` — teď hlavně
věz, *proč* to existuje: je to záplata na to, že defaultně je v Reactu
každý render úplně čistý stůl.

## `useRef` — jediná skutečná "proměnná" mezi rendery

Jedno místo, kde React nabízí něco blízkého Vue mutovatelnému refu, je
`useRef`. Na rozdíl od `useState` změna `.current` **nevyvolá** nový
render — je to prostě box, který přežije mezi rendery, beze změny identity:

```tsx
const renderCount = useRef(0)
renderCount.current += 1 // mutace přímo, žádný setter, žádný re-render
```

Tohle je nejblíž tomu, na co jsi zvyklý z Vue (mutovatelná hodnota, co
"prostě je"), ale záměrně se nepoužívá jako náhrada za `useState` — pokud
změna má ovlivnit, co se vykreslí, patří do `useState`. `useRef` je pro
věci, co UI přímo neřídí (ID timeru, reference na DOM element, "poslední
viděná hodnota" pro porovnání). Podrobně na to dojde v `05-refs-a-dom`.

## Praktický checklist

Když se něco v Reactu chová "divně" — zamrzlo to, zapomnělo se to, resetlo
se to — zeptej se:

1. **Kde tahle closure vznikla?** Handler/efekt/callback vidí hodnoty
   z renderu, ve kterém byl vytvořený — ne "aktuální" hodnoty.
2. **Je to `useState`/`useRef`, nebo obyčejná proměnná v těle funkce?**
   Obyčejná proměnná nepřežije do dalšího renderu. Pokud potřebuješ, aby
   něco přežilo, musí to být v hooku.
3. **Má `useEffect` úplné dependency pole?** Chybějící závislost = efekt
   uvnitř pracuje se zastaralými hodnotami donekonečna (dokud se efekt
   z jiného důvodu nepřezaloží).
4. **Potřebuju stabilní identitu objektu/funkce napříč rendery?** Pokud
   ano (kvůli `useEffect` dependencím nebo `React.memo`), budeš chtít
   `useMemo`/`useCallback` — ne teď nutně, ale věz, že na to existuje
   řešení.

Vue model: postav graf jednou, mutuj hodnoty uvnitř. React model: přepočítej
všechno znovu při každém renderu, a jen to, co explicitně vložíš do
`useState`/`useRef`/`useReducer`, přežije do dalšího kola.

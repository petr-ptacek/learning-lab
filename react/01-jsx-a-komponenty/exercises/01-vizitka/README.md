# 01 — Vizitka

Napiš svou první React komponentu.

## Požadavky

- Napiš function komponentu `ProfileCard`, která přijme props `name`, `role`
  a `email` a vykreslí je do JSX. Typ props popiš přes `interface`.
- V `App` vykresli `ProfileCard` s konkrétními hodnotami (props napevno v kódu).
- Vykreslený obsah např. pro `name="Petr Ptáček"`, `role="Frontend Developer"`,
  `email="petr@example.com"`:

```
Petr Ptáček
Frontend Developer
petr@example.com
```

### Příklady props → vykreslený obsah

| name          | role               | email                  | Vykreslený obsah                                            |
|---------------|--------------------|------------------------|-------------------------------------------------------------|
| Petr Ptáček   | Frontend Developer | petr@example.com       | `Petr Ptáček` / `Frontend Developer` / `petr@example.com`   |
| Jana Nováková | UX Designer        | jana.novakova@firma.cz | `Jana Nováková` / `UX Designer` / `jana.novakova@firma.cz`  |
| Karel Svoboda | Backend Developer  | karel@svoboda.dev      | `Karel Svoboda` / `Backend Developer` / `karel@svoboda.dev` |

## Bonus

- Rozděl vizitku na dvě komponenty: `ProfileCard` (jméno + role) a
  `ContactInfo` (email). `ContactInfo` vlož jako `children` dovnitř
  `ProfileCard` — vyzkoušíš si tak kompozici komponent.

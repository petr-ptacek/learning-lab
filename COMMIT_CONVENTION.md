# Commit konvence

Formát (zjednodušené [Conventional Commits](https://www.conventionalcommits.org/)):

```
type(scope): stručný popis v přítomném čase
```

## Type

- `feat` — nový obsah (nové téma, teorie, cvičení, vyřešené cvičení)
- `fix` — oprava chyby v existujícím obsahu/kódu
- `docs` — úpravy README/dokumentace, které nejsou `feat`
- `chore` — repo housekeeping (`.gitignore`, struktura, konfigurace)
- `refactor` — přeorganizování obsahu beze změny významu

## Scope

Název tématu, kterého se commit týká: `python`, `django`, `vue`, `react`,
`projects`, `template`. Pro změny napříč celým repem scope vynech.

## Příklady

```
feat(python): add basics theory and starter exercises
feat(python): solve 01-osobni-vizitka exercise
fix(react): correct wrong hook example in theory
docs(vue): add resources for components topic
chore: add .gitignore
refactor: split THEORY.md into theory/ folder
```

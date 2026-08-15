# 04 — Tabulka známek

Napiš skript, který načte 3 předměty se známkami a vypíše je jako zarovnanou
tabulku spolu s průměrem.

## Požadavky

- Načti postupně 3x dvojici (název předmětu, známka 1–5) — každou dvojici
  samostatnými `input()` voláními (cyklus přijde na řadu v dalším tématu).
- Spočítej průměr známek, zaokrouhlený na 2 desetinná místa.
- Výstup zarovnej pomocí formátovacího mini-jazyka — název předmětu doleva,
  známka doprava, na pevnou šířku sloupce (viz `THEORY.md` → Formátovací
  mini-jazyk), např.:

```
--- Vysvědčení ---
Předmět         Známka
Matematika           1
Čeština              2
Angličtina           1
------------------------
Průměr:            1.33
```

## Požadavky na formátování

- Sloupec s předmětem: doleva, pevná šířka (např. `{predmet:<15}`).
- Sloupec se známkou: doprava, pevná šířka (např. `{znamka:>6}`).
- Průměr: 2 desetinná místa (`.2f`).

## Bonus

- Záhlaví tabulky ("Předmět", "Známka") zarovnej na střed pomocí `^`.
- Délku oddělovací čáry (`---...`) odvoď z délky nejdelšího řádku místo
  napevno napsaného počtu znaků.

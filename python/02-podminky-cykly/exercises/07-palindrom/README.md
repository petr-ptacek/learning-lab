# 07 — Palindrom

Napiš skript, který zjistí, jestli je zadaný text palindrom (čte se stejně
odpředu i odzadu) — **bez** použití obráceného řetězce naráz (`[::-1]` nebo
`reversed()`), ale pomocí cyklu, který porovnává znaky od začátku a od
konce.

## Požadavky

- Načti text pomocí `input()`.
- Použij dva indexy — jeden začíná na prvním znaku, druhý na posledním —
  a `while` cyklus, který je postupně posouvá k sobě, dokud se nepotkají.
- V každé iteraci porovnej znaky na obou indexech. Pokud se neshodují,
  `break` cyklus a vypiš, že text není palindrom.
- Pokud cyklus doběhne bez neshody, vypiš, že text je palindrom.
- Výstup např.:

```
Zadej text: kajak
"kajak" je palindrom
```

### Příklady vstup/výstup

| Vstup | Výstup |
|---|---|
| `kajak` | `"kajak" je palindrom` |
| `level` | `"level" je palindrom` |
| `python` | `"python" není palindrom` |
| `a` | `"a" je palindrom` |
| `ab` | `"ab" není palindrom` |

## Bonus

- Ignoruj mezery a velikost písmen (např. `"Kobyla ma malý bok"` je po
  odstranění mezer a s malými písmeny palindrom).

### Příklady vstup/výstup (bonus)

| Vstup | Výstup |
|---|---|
| `Kobyla ma malý bok` | `je palindrom` |
| `Jelenovi pivo nelej` | `je palindrom` |
| `Ahoj svete` | `není palindrom` |

# Ruff — linter a formatter pro Python

## Co to je

[Ruff](https://docs.astral.sh/ruff/) je **linter i formatter** pro Python.
Je od stejné firmy jako uv (Astral), taky napsaný v Rustu, a díky tomu
extrémně rychlý. Za posledních pár let se stal de facto standardem a
nahradil celou sadu starších nástrojů:

| Dřív | Co to dělalo | V Ruffu |
|---|---|---|
| `flake8` (+ desítky pluginů) | linting: chyby, nepoužité importy, … | `ruff check` |
| `isort` | řazení importů | `ruff check` (pravidla `I`) |
| `pyupgrade` | přepis na moderní syntaxi | `ruff check` (pravidla `UP`) |
| `black` | formátování kódu | `ruff format` |

## Mentální model přes FE

| FE | Python |
|---|---|
| ESLint | `ruff check` |
| Prettier | `ruff format` |
| `eslint --fix` | `ruff check --fix` |
| `.eslintrc` / `eslint.config.js` | sekce `[tool.ruff]` v `pyproject.toml` |
| ESLint pluginy (`eslint-plugin-vue`) | sady pravidel (`DJ` = Django, `B` = bugbear, …) |

Stejně jako u ESLint + Prettier jde o dvě různé věci:

- **Linter** (`ruff check`) hledá *problémy*: nepoužitý import, nedefinovaná
  proměnná, podezřelý vzor, který bývá bug. Část umí opravit sám (`--fix`).
- **Formatter** (`ruff format`) řeší jen *vzhled*: uvozovky, odsazení,
  zalamování řádků. Nemění, co kód dělá, a nediskutuje se o něm.
  Styl je kompatibilní s Blackem, takže stejný kód uvidíš i v projektech,
  které ještě používají Black.

## Příkazy

```bash
uv add --dev ruff              # přidá jako vývojovou závislost

uv run ruff check .            # najdi problémy
uv run ruff check --fix .      # oprav, co jde opravit automaticky
uv run ruff format .           # přeformátuj kód
uv run ruff format --check .   # jen zkontroluj (v CI), nic neměň
uv run ruff rule DJ008         # vysvětlení konkrétního pravidla
```

Výstup `ruff check` vypadá takhle. Každé hlášení má kód pravidla
(`F401`, `DJ008`, …), podle kterého si ho dohledáš:

```
F401 [*] `django.test.TestCase` imported but unused
 --> tasks/tests.py:1:25
DJ008 Model does not define `__str__` method
 --> tasks/models.py:4:7
```

`[*]` = opravitelné přes `--fix`.

## Konfigurace

Píše se do `pyproject.toml`, nepotřebuješ žádný další soubor:

```toml
[tool.ruff]
extend-exclude = ["*/migrations/*"]   # migrace generuje Django, nelintujeme je

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "DJ"]
ignore = ["E501"]                     # délku řádků hlídá formatter
```

Co znamenají vybrané sady pravidel:

| Kód | Původ | Co hlídá |
|---|---|---|
| `E` | pycodestyle | základní stylové chyby |
| `F` | Pyflakes | skutečné chyby: nepoužité importy/proměnné, nedefinovaná jména |
| `I` | isort | pořadí a seskupení importů |
| `UP` | pyupgrade | zastaralá syntaxe, když jde napsat moderněji |
| `B` | flake8-bugbear | časté zdroje bugů (např. mutable default argument) |
| `DJ` | flake8-django | Django specifika: `__str__` u modelu, `null=True` u textových polí, … |

Kompletní seznam: [Rules](https://docs.astral.sh/ruff/rules/).
V pracovních projektech uvidíš podobnou sekci `[tool.ruff]`. Když ti CI
spadne na Ruffu, kód pravidla ti řekne proč.

## Jak to používáme v tomhle repu

- Ruff je v každém cvičení jako dev závislost, konfigurace je v
  `pyproject.toml` (viz výše). Scaffold cvičení je předem přeformátovaný a
  prochází `ruff check` bez chyb.
- Než dáš řešení ke kontrole, pusť:

  ```bash
  uv run ruff format . && uv run ruff check .
  ```

  Bere se to jako součást řešení, stejně jako by to po tobě chtělo CI
  v práci.
- Editor: rozšíření **Ruff** pro VS Code / vestavěná podpora v PyCharm
  (Settings → Tools → Ruff) umí formátovat při uložení, podobně jako
  Prettier.

## Odkazy

- [Ruff — dokumentace](https://docs.astral.sh/ruff/)
- [Linter](https://docs.astral.sh/ruff/linter/) a
  [Formatter](https://docs.astral.sh/ruff/formatter/)
- [Seznam pravidel](https://docs.astral.sh/ruff/rules/)
- [Konfigurace](https://docs.astral.sh/ruff/configuration/)

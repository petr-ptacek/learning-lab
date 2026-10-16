# uv — správa Python projektů a závislostí

## Co to je a proč

[uv](https://docs.astral.sh/uv/) je správce balíčků a projektů pro Python
(napsaný v Rustu, od Astral — autorů linteru Ruff). Jeden nástroj nahrazuje
celou sadu starších:

| Dřív                             | Na co                           | V uv                    |
|----------------------------------|---------------------------------|-------------------------|
| `pip`                            | instalace balíčků               | `uv add`, `uv sync`     |
| `venv` / `virtualenv`            | izolované prostředí pro projekt | `.venv/` vytváří uv sám |
| `pip-tools` / `requirements.txt` | zamčené verze                   | `uv.lock`               |
| `pyenv`                          | instalace verzí Pythonu         | `uv python install`     |
| `pipx`                           | globální CLI nástroje           | `uv tool`               |

Proč to vadilo dřív: `pip install` instaluje do *aktuálně aktivního*
Pythonu. Když zapomeneš aktivovat venv, balíček skončí globálně.
`requirements.txt` je jen seznam a sám verze tranzitivních závislostí
nezamyká. uv tohle řeší stejně jako npm: projekt má manifest a lockfile
a `.venv` ve složce projektu.

## Mentální model přes npm

| npm                        | uv                    |
|----------------------------|-----------------------|
| `package.json`             | `pyproject.toml`      |
| `package-lock.json`        | `uv.lock`             |
| `node_modules/`            | `.venv/`              |
| `.nvmrc`                   | `.python-version`     |
| `npm init`                 | `uv init`             |
| `npm install`              | `uv sync`             |
| `npm install axios`        | `uv add django`       |
| `npm install -D vitest`    | `uv add --dev pytest` |
| `npm uninstall axios`      | `uv remove django`    |
| `npx vite` / `npm run dev` | `uv run …`            |

Jeden rozdíl oproti npm: `.venv/` obsahuje **i samotný Python
interpreter** (resp. odkaz na něj), ne jen balíčky. Proto se dřív venv
„aktivoval“ (`source .venv/bin/activate`), aby příkaz `python` ukazoval
na ten správný. S uv to nepotřebuješ: `uv run` spustí příkaz rovnou
v prostředí projektu.

## Soubory v projektu

```toml
# pyproject.toml — manifest projektu (standard PEP 621, není specifický pro uv)
[project]
name = "solution"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "django>=6.1.2",
]
```

- `uv.lock` — přesné verze všech závislostí včetně tranzitivních.
  **Commituje se**, ručně se needituje.
- `.python-version` — verze Pythonu pro projekt (`3.14`). Commituje se.
- `.venv/` — nainstalované prostředí. **Necommituje se** (je v
  `.gitignore`), dá se kdykoliv znovu vytvořit přes `uv sync`.

## Základní příkazy

```bash
# Nový projekt (--bare = jen pyproject.toml, bez ukázkového main.py a README)
uv init --bare
uv python pin 3.14          # vytvoří .python-version

# Závislosti
uv add django               # přidá do pyproject.toml, zamkne, nainstaluje
uv add djangorestframework
uv add --dev pytest         # vývojová závislost (obdoba devDependencies)
uv remove django

# Instalace podle lockfilu (po git clone / pull)
uv sync

# Spouštění v prostředí projektu
uv run manage.py runserver  # = python manage.py runserver uvnitř .venv
uv run python               # interaktivní Python s nainstalovanými balíčky
uv run django-admin startproject config .

# Přehled
uv tree                     # strom závislostí (obdoba npm ls)
uv pip list                 # co je nainstalované ve .venv
```

`uv run` před spuštěním zkontroluje, že `.venv` odpovídá `uv.lock`, a
případně ho dosynchronizuje. Po pullu tedy většinou ani nemusíš ručně
volat `uv sync`.

## Víc verzí Pythonu na jednom stroji

uv umí stáhnout a spravovat vlastní verze Pythonu, podobně jako `nvm`
u Node. Ukládá je do `~/.local/share/uv/python/` a systémový Python
(`/usr/bin/python3`) nechává na pokoji:

```bash
uv python list              # co je nainstalované a co je k dispozici
uv python install 3.14      # stáhne Python 3.14
uv python pin 3.14          # projekt bude používat 3.14 (.python-version)
```

Když projekt v `.python-version` požaduje verzi, kterou na stroji nemáš,
`uv sync` / `uv run` ji stáhne automaticky. Každý projekt tak může mít
jinou verzi a navzájem se neovlivňují.

## Jak to používáme v tomhle repu

Každé cvičení (`solution/` i `reference/`) je samostatný uv projekt.
Typický postup:

```bash
cd django/01-.../exercises/01-.../solution
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

## Odkazy

- [uv — dokumentace](https://docs.astral.sh/uv/)
- [Working on projects](https://docs.astral.sh/uv/guides/projects/) — návod
  na projekty, `uv add`/`uv run`/`uv sync`
- [Migrace z pip](https://docs.astral.sh/uv/guides/migration/pip-to-project/)
  — pokud v práci narazíš na `requirements.txt`

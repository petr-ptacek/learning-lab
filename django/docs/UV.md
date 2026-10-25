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

## Instalace

uv se instaluje **globálně, jednou na stroj**, ne do projektu (obdoba
`nvm`, ne `npm install`). Nepotřebuje k tomu žádný Python, je to
samostatná binárka.

Oficiální instalátor (Linux / macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Uloží `uv` a `uvx` do `~/.local/bin/`, nic nevyžaduje `sudo`. Tahle
složka už v `PATH` je, takže po otevření nového terminálu stačí ověřit:

```bash
uv --version
```

Pokud shell `uv` nenajde, chybí `~/.local/bin` v `PATH`. Instalátor
na konci vypíše, co přidat do `~/.zshrc`.

Další užitečné kroky:

```bash
uv self update              # aktualizace na nejnovější verzi

# doplňování příkazů tabulátorem v zsh
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
```

**Nedělej `pip install uv`** do systémového Pythonu. Debian/Ubuntu to
stejně zablokuje (`externally-managed-environment`) a `uv self update`
by pak nefungoval. Další způsoby (`pipx`, Homebrew, Windows) jsou v
[Installing uv](https://docs.astral.sh/uv/getting-started/installation/).

Odinstalace:

```bash
uv cache clean
rm -r "$(uv python dir)" "$(uv tool dir)"   # Pythony a nástroje stažené přes uv
rm ~/.local/bin/uv ~/.local/bin/uvx
```

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

### Pozor na pyenv: holý `python` v uv projektu

Na stroji je nainstalovaný i **pyenv**. Ten podstrčí vlastní příkaz `python`
(shim v `~/.pyenv/shims/`), který se podívá do `.python-version`
v aktuální složce a hledá tu verzi **ve svém** úložišti. Verzi
nainstalovanou přes uv nezná, proto v uv projektu:

```
$ python
pyenv: version `3.14' is not installed (set by .../solution/.python-version)
```

Nejde o chybu v projektu. `.python-version` je společná konvence, kterou
čte pyenv i uv, a každý si verzi hledá jinde. Řešení:

```bash
uv run python              # ✅ doporučeno: Python z .venv projektu, pyenv se obejde
uv run manage.py shell     # totéž pro Django příkazy

source .venv/bin/activate  # alternativa: aktivace venv,
python --version           #   pak `python` ukazuje do .venv
deactivate
```

Holý `python` / `pip` ve uv projektu nepoužívej, vždycky přes `uv run`.

## Nastavení PyCharmu

PyCharm má na projekt jeden interpreter, ale každé cvičení má vlastní
`.venv`. Když máš otevřené celé repo `learning-lab`, nastav pro aktuální
cvičení dvě věci:

1. **Interpreter**: Settings → Project: learning-lab → Python Interpreter →
   Add Interpreter → Add Local Interpreter → Type: **uv** → Select
   existing → `…/exercises/NN-…/solution/.venv/bin/python`. Cestu
   k binárce uv (`~/.local/bin/uv`) PyCharm najde sám. V seznamu balíčků
   pak musí být `django` a `ruff`.
2. **Sources Root**: pravým tlačítkem na `solution/` → Mark Directory as →
   Sources Root (nebo Settings → Project Structure). Importy `config` a
   `pages` se tak hledají od `solution/`, stejně jako při
   `uv run manage.py`.

**Proč typ uv, ne Virtualenv / Python:** uv do `.venv` neinstaluje `pip`.
PyCharm u obyčejného venv čte seznam balíčků přes `pip`, takže by ukázal
„Nothing to show“, i když `django` v `.venv` je (napovídání by
fungovalo, chybí jen seznam). S typem uv se ptá přes `uv pip list`.
`pip` do `.venv` neinstaluj, další `uv sync` by ho zase odebral.

U dalšího cvičení obojí přepni na jeho `solution/` a starý Sources Root
odeber (křížkem v Project Structure), aby se cvičení nepletla.

**Proč na tom záleží:** v kořeni repa je složka `django/` (tohle téma).
PyCharm přidává kořen projektu do cesty pro importy a Python bere i
složku bez `__init__.py` jako balíček. Se špatně nastaveným interpreterem
proto `import django` trefí tuhle složku místo knihovny a PyCharm hlásí:

```
Cannot find reference 'core' in 'imported module django'
```

Při skutečném běhu (`uv run` ze `solution/`) problém nenastane, jde čistě
o analýzu kódu v IDE.

**Alternativa:** File → Open… → `solution/` → New Window. Kořenem projektu
je pak rovnou `solution/`, PyCharm najde `.venv` sám (případně ho vyber
ve stejném dialogu jako výše) a není potřeba nic přepínat.

**Ruff:** Settings → Python → Tools → External Tools → Ruff **ON** a v
Tools → Actions on Save zaškrtnout *Reformat code* a *Optimize imports*
(jen pro Python). Podrobně v [`RUFF.md`](RUFF.md#nastavení-pycharmu).

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

# 08 — OOP: dědičnost — zdroje

## V tomhle repu

Výtah z článků níže, česky a s ověřenými ukázkami:

- [`../docs/INHERITANCE_AND_SUPER.md`](../docs/INHERITANCE_AND_SUPER.md)
  — dědičnost, hledání atributů přes rodiče, přepsání metody,
  `super()`, atributy třídy jako konfigurace, `isinstance`, kompozice
- [`../docs/MULTIPLE_INHERITANCE_AND_MIXINS.md`](../docs/MULTIPLE_INHERITANCE_AND_MIXINS.md)
  — MRO, diamant, kooperativní `super()`, mixiny, Django views
- [`../docs/ABSTRACT_BASE_CLASSES.md`](../docs/ABSTRACT_BASE_CLASSES.md)
  — `ABC`, `@abstractmethod`, template method, `collections.abc`,
  `Protocol`
- [`../docs/DESCRIPTORS.md`](../docs/DESCRIPTORS.md) — protokol
  deskriptorů, pořadí hledání atributu, `property` a pole modelu
- [`../docs/CLASS_CREATION_AND_METACLASSES.md`](../docs/CLASS_CREATION_AND_METACLASSES.md)
  — vytvoření třídy, `__init_subclass__`, metatřídy, jak vzniká Django
  model a jeho `_meta`
- [`../docs/ENUMS.md`](../docs/ENUMS.md) — `Enum`, `IntEnum` /
  `StrEnum`, `auto`, metody na enumu, hodnota s popiskem, Django
  `TextChoices` / `IntegerChoices`

## Oficiální dokumentace

- [Tutorial — Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
  a [Multiple Inheritance](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance)
- [`super()`](https://docs.python.org/3/library/functions.html#super),
  [`isinstance`](https://docs.python.org/3/library/functions.html#isinstance),
  [`issubclass`](https://docs.python.org/3/library/functions.html#issubclass)
- [The Python 2.3 Method Resolution Order](https://docs.python.org/3/howto/mro.html)
  — jak se počítá MRO (C3), do hloubky
- [`abc`](https://docs.python.org/3/library/abc.html) a
  [`collections.abc`](https://docs.python.org/3/library/collections.abc.html)
  — tabulka „abstraktní metody → co dostaneš zdarma“
- [Descriptor Guide](https://docs.python.org/3/howto/descriptor.html)
  — oficiální průvodce deskriptory, včetně toho, jak jsou napsané
  `property`, `classmethod` a metody
- [Data model — Customizing class creation](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation)
  — `__init_subclass__`, `__set_name__`, metatřídy
- [`enum`](https://docs.python.org/3/library/enum.html) a
  [Enum HOWTO](https://docs.python.org/3/howto/enum.html) — návod
  s příklady, včetně vlastního `__new__` a `_missing_`

## Články / tutoriály

- [Real Python — Inheritance and Composition: A Python OOP Guide](https://realpython.com/inheritance-composition-python/)
- [Real Python — Supercharge Your Classes With Python super()](https://realpython.com/python-super/)
- [Raymond Hettinger — Python's super() considered super!](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)
  — klasika o kooperativním `super()` a mixinech
- [Real Python — Implementing an Interface in Python](https://realpython.com/python-interface/)
  — `abc`, neformální vs. formální rozhraní
- [Real Python — Python Protocols: Leveraging Structural Subtyping](https://realpython.com/python-protocol/)
- [Real Python — Python Descriptors: An Introduction](https://realpython.com/python-descriptors/)
- [Real Python — Python Metaclasses](https://realpython.com/python-metaclasses/)
- [Real Python — Build Enumerations of Constants With Python's Enum](https://realpython.com/python-enum/)

## Souvislost s Djangem

- [Django — Model inheritance](https://docs.djangoproject.com/en/6.1/topics/db/models/#model-inheritance)
  — abstraktní základ, multi-table, proxy modely, dědění `Meta`
- [Django — Model Meta options](https://docs.djangoproject.com/en/6.1/ref/models/options/)
  — všechno, co jde napsat do `class Meta`
- [Django — Enumeration types](https://docs.djangoproject.com/en/6.1/ref/models/fields/#enumeration-types)
  — `TextChoices`, `IntegerChoices`, `label`, `.choices`
- [Django — Using mixins with class-based views](https://docs.djangoproject.com/en/6.1/topics/class-based-views/mixins/)
- [Classy Class-Based Views](https://ccbv.co.uk/) — pro každou
  Django view ukáže MRO a odkud je která metoda

## Pro srovnání z JS

- [MDN — extends](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/extends)
- [MDN — super](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/super)

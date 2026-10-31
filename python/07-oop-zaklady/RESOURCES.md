# 07 — OOP: základy — zdroje

## V tomhle repu

Výtah z článků níže, česky a s ověřenými ukázkami:

- [`../docs/CLASSES_AND_INSTANCES.md`](../docs/CLASSES_AND_INSTANCES.md)
  — hledání atributů, třída vs. instance, `self`, `getattr` / `setattr`,
  třída jako objekt, vnořená třída, srovnání s JS
- [`../docs/METHODS_AND_PROPERTIES.md`](../docs/METHODS_AND_PROPERTIES.md)
  — instanční / třídní / statické metody, alternativní konstruktory,
  `@property`, `cached_property`
- [`../docs/DUNDER_METHODS.md`](../docs/DUNDER_METHODS.md) — `__str__`
  vs. `__repr__`, `__eq__` a `__hash__`, řazení, operátory,
  `NotImplemented`, kontejnerový protokol
- [`../docs/DATACLASSES.md`](../docs/DATACLASSES.md) — `@dataclass`,
  `field`, `frozen`, `order`, `__post_init__`, `asdict`, srovnání
  s `TypedDict` a Django modelem

## Oficiální dokumentace

- [Tutorial — Classes](https://docs.python.org/3/tutorial/classes.html)
  — celá kapitola, hlavně 9.3 (první třídy) a 9.4 (atributy třídy vs.
  instance, past se sdíleným seznamem)
- [Data model — Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)
  — referenční seznam všech dunder metod
- [`property`](https://docs.python.org/3/library/functions.html#property),
  [`classmethod`](https://docs.python.org/3/library/functions.html#classmethod),
  [`staticmethod`](https://docs.python.org/3/library/functions.html#staticmethod)
- [`functools.cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property)
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)

## Články / tutoriály

- [Real Python — Python Classes: The Power of Object-Oriented Programming](https://realpython.com/python-classes/)
- [Real Python — Object-Oriented Programming (OOP) in Python](https://realpython.com/python3-object-oriented-programming/)
- [Real Python — Python's Instance, Class, and Static Methods Demystified](https://realpython.com/instance-class-and-static-methods-demystified/)
- [Real Python — Python's property(): Add Managed Attributes to Your Classes](https://realpython.com/python-property/)
- [Real Python — Python's Magic Methods: Leverage Their Power in Your Classes](https://realpython.com/python-magic-methods/)
- [Real Python — When Should You Use .__repr__() vs .__str__() in Python?](https://realpython.com/python-repr-vs-str/)
- [Real Python — Data Classes in Python](https://realpython.com/python-data-classes/)

## Souvislost s Djangem

- [Django — Models](https://docs.djangoproject.com/en/6.1/topics/db/models/)
  — po tomhle konceptu přečti znovu: pole jako atributy třídy,
  `class Meta`, metody modelu, `__str__`, `@property`

## Pro srovnání z JS

- [MDN — Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes)
- [MDN — getter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get)
  / [setter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/set)
  — obdoba `@property`

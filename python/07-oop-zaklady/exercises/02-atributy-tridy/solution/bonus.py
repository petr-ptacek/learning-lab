from collections.abc import Sequence


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def describe(obj: object, fields: Sequence[str]) -> dict[str, str | None]:
    return {field: getattr(obj, field, None) for field in fields}


p = Person("Joe Doe", 19)

print(describe(p, ("name", "age", "unknown")))


def update(obj: object, **changes):
    for field, value in changes.items():
        setattr(obj, field, value)


update(p, name="Jonathan", age=20)
print(describe(p, ("name", "age")))

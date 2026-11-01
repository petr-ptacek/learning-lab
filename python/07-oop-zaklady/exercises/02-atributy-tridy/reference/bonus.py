from collections.abc import Iterable
from typing import Any


class Ticket:
    next_id = 1
    priority = "normal"

    def __init__(self, title: str, priority: str | None = None) -> None:
        self.id = Ticket.next_id
        Ticket.next_id += 1
        self.title = title
        if priority is not None:
            self.priority = priority


def describe(obj: object, fields: Iterable[str]) -> dict[str, Any]:
    return {field: getattr(obj, field, None) for field in fields}


def update(obj: object, **changes: Any) -> None:
    for name, value in changes.items():
        setattr(obj, name, value)


t1 = Ticket("Nejde přihlášení")
t2 = Ticket("Pomalý web", "high")
print(describe(t2, ["id", "title", "priority"]))
print(describe(t1, ["id", "priority", "author"]))
print(describe(t1, []))
update(t1, title="Opraveno", status="done")
print(vars(t1))

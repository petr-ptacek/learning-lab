import json
from dataclasses import asdict, dataclass, field, replace


@dataclass
class Product:
    name: str
    price: float
    quantity: int = field(default=0)
    tags: list[str] = field(default_factory=list)

    def total_value(self):
        return self.price * self.quantity


p = Product(name="Mléko", price=1)
# print(asdict(p))
print(json.dumps(asdict(p), ensure_ascii=False))


p_1 = replace(p, price=100, quantity=100, tags=["a", "b", "c"])
print(json.dumps(asdict(p_1), ensure_ascii=False))


@dataclass
class User:
    username: str
    password: str = field(repr=False)
    is_active: bool = field(default=True)


print(User(username="john", password="password"))

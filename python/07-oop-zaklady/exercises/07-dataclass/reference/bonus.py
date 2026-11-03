import json
from dataclasses import asdict, dataclass, field, replace


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    tags: list[str] = field(default_factory=list)


@dataclass
class User:
    username: str
    password: str = field(repr=False)
    is_active: bool = True


coffee = Product("Káva", 189.0, 3, ["bio"])
data = asdict(coffee)
print(data)
print(json.dumps(data, ensure_ascii=False))

cheaper = replace(coffee, price=169.0)
print(coffee.price, cheaper.price)  # 189.0 169.0

user = User("anna", "tajne123")
print(user)  # User(username='anna', is_active=True)
print(user.password)  # tajne123

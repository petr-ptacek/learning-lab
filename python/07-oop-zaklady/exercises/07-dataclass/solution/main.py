import math
from dataclasses import asdict, dataclass, field


@dataclass
class Product:
    name: str
    price: float
    quantity: int = field(default=0)
    tags: list[str] = field(default_factory=list)

    def total_value(self):
        return self.price * self.quantity


p = Product(name="Mleko", price=1)

# Předpověď: co se stane, když napíšeš tags: list[str] = []
# vyhodi to chybu, protoze se tvori class attribut, ktery pak sdileji vsechny instance, a pokud by nekdo pouzit append, tak zmeni vsechny instance
# je treba tedy factory


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other):
        return round(math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2), 2)


print({Point(1, 2), Point(3, 4)})


@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int = field(default=0)

    @classmethod
    def parse(cls, text: str):
        return cls(*map(int, text.split(".")))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


version_1 = Version.parse("1.12")
version_2 = Version.parse("1.15.0")
print(version_1)


@dataclass
class Email:
    address: str

    def __post_init__(self):
        self.address = self.address.strip().lower()

    @property
    def domain(self):
        return self.address.split("@")[1] if "@" in self.address else ""


print(Email("A@B.cz") == Email("a@b.CZ "))

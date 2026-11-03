import math
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    # tags: list[str] = [] → ValueError: mutable default <class 'list'> for
    # field tags is not allowed. Výchozí hodnota leží na třídě a všechny
    # instance by sdílely jeden seznam (jako Cart ve cvičení 02).
    tags: list[str] = field(default_factory=list)

    def total_value(self) -> float:
        return round(self.price * self.quantity, 2)


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return round(math.hypot(self.x - other.x, self.y - other.y), 2)


@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int = 0

    @classmethod
    def parse(cls, text: str) -> "Version":
        return cls(*map(int, text.split(".")))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class Email:
    address: str

    def __post_init__(self) -> None:
        self.address = self.address.strip().lower()

    @property
    def domain(self) -> str:
        return self.address.partition("@")[2]


print(Product("Mléko", 24.9, 10))
print(Product("Mléko", 24.9, 10).total_value())  # 249.0

print(Point(0, 0).distance_to(Point(3, 4)))  # 5.0
print(len({Point(0, 0), Point(1, 2), Point(0, 0)}))  # 2

# Stringy se porovnávají znak po znaku ("1" < "9"), order=True porovnává
# tuple polí: (1, 10, 0) > (1, 9, 3).
print(Version.parse("1.10.0") > Version.parse("1.9.3"), "1.10.0" > "1.9.3")
print([str(v) for v in sorted(map(Version.parse, ["1.10.0", "1.2.3", "1.9.3", "0.9"]))])

email = Email("  Anna.Novakova@Example.CZ ")
print(email, email.domain)

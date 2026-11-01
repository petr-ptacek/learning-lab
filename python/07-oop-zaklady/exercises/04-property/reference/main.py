class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @property
    def fahrenheit(self) -> float:
        return round(self.celsius * 9 / 5 + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = round((value - 32) * 5 / 9, 2)

    @property
    def kelvin(self) -> float:
        return round(self.celsius + 273.15, 2)


class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, value: str) -> None:
        self.first_name, self.last_name = value.split(" ", 1)

    @property
    def initials(self) -> str:
        return f"{self.first_name[0]}. {self.last_name[0]}."


class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price  # jde přes setter → validace platí i tady

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Cena nesmí být záporná")
        self._price = round(value, 2)


t = Temperature(25)
print(t.fahrenheit, t.kelvin)  # 77.0 298.15
t.fahrenheit = 212
print(t.celsius)  # 100.0
# t.kelvin = 0 → AttributeError: property bez setteru je jen pro čtení.
# t.fahrenheit() → TypeError: t.fahrenheit už je float, závorky ho volají.

p = Person("Anna", "Nováková")
p.full_name = "Jan Amos Komenský"
print(p.first_name, p.last_name, p.initials)  # Jan Amos Komenský J. A.

x = Product("Mléko", 24.999)
print(x.price, vars(x))  # 25.0 {'name': 'Mléko', '_price': 25.0}

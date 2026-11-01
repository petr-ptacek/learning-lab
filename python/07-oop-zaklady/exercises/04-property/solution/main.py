class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return round((self.celsius * 1.8) + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) / 1.8

    @property
    def kelvin(self):
        return round(self.celsius + 273.15, 2)


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, full_name: str):
        f, l = full_name.split(maxsplit=1)
        self.first_name = f
        self.last_name = l

    @property
    def initials(self):
        return f"{self.first_name[:1]}. {self.last_name[:1]}."


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("Cena nesmí být záporná")

        self._price = round(price, 2)


temp = Temperature(38)
print(temp.fahrenheit)
print(temp.kelvin)

joe = Person("Joe", "Smith")
print(joe.full_name)

product = Product("mleko", 40)
print(product.price)

product.price = -50

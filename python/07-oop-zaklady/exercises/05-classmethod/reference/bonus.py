class Book:
    objects: list["Book"] = []

    def __init__(self, title: str, author: str, year: int) -> None:
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self) -> str:
        return f"Book({self.title!r})"

    @classmethod
    def create(cls, **fields) -> "Book":
        book = cls(**fields)
        cls.objects.append(book)
        return book

    @classmethod
    def all(cls) -> list["Book"]:
        return list(cls.objects)

    @classmethod
    def filter(cls, **conditions) -> list["Book"]:
        missing = object()
        return [
            book
            for book in cls.objects
            if all(getattr(book, name, missing) == value for name, value in conditions.items())
        ]

    @classmethod
    def count(cls) -> int:
        return len(cls.objects)


Book.create(title="R.U.R.", author="Čapek", year=1920)
Book.create(title="Krakatit", author="Čapek", year=1924)
Book.create(title="Saturnin", author="Jirotka", year=1942)

print(Book.count())  # 3
print(Book.filter(author="Čapek"))  # [Book('R.U.R.'), Book('Krakatit')]
print(Book.filter(author="Čapek", year=1924))  # [Book('Krakatit')]
print(Book.filter())  # všechny tři: all() z prázdné sekvence je True
Book("Mimo", "X", 2000)
Book.all().clear()
print(Book.count())  # 3

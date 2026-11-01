class Book:
    objects = []

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return f"Book({self.title!r})"

    @classmethod
    def create(cls, **fields):
        instance = cls(**fields)
        cls.objects.append(instance)

        return instance

    @classmethod
    def all(cls):
        return cls.objects.copy()

    @classmethod
    def filter(cls, **conditions):
        def fn(book):
            for condition, value in conditions.items():
                if not (hasattr(book, condition) and getattr(book, condition) == value):
                    return False

            return True

        return [book for book in cls.objects if fn(book)]

    @classmethod
    def count(cls):
        return len(cls.objects)


Book.create(title="R.U.R.", author="Čapek", year=1920)
Book.create(title="Krakatit", author="Čapek", year=1924)
Book.create(title="Saturnin", author="Jirotka", year=1942)

print(Book.count())
print(Book.all())
print(Book.filter(title="Saturnin"))
print(Book.filter())
Book.all().clear()
print(Book.count())

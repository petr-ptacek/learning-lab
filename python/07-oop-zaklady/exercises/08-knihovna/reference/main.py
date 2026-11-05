from collections.abc import Iterable, Iterator
from dataclasses import dataclass

RECORDS = [
    {"isbn": "111", "title": "R.U.R.", "author": "Karel Čapek", "year": 1920},
    {"isbn": "222", "title": "Krakatit", "author": "Karel Čapek", "year": 1924},
    {"isbn": "333", "title": "Saturnin", "author": "Zdeněk Jirotka", "year": 1942},
    {"isbn": "444", "title": "Babička", "author": "Božena Němcová", "year": 1855},
]


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    year: int
    available: bool = True

    def __str__(self) -> str:
        return f"{self.title} ({self.author}, {self.year})"


class Member:
    max_books = 2

    def __init__(self, name: str, max_books: int | None = None) -> None:
        self.name = name
        self.borrowed: list[Book] = []
        if max_books is not None:
            self.max_books = max_books  # zastíní limit třídy jen pro tuto instanci

    def can_borrow(self) -> bool:
        return len(self.borrowed) < self.max_books


class Library:
    def __init__(self, books: Iterable[Book] = ()) -> None:
        self._books = {book.isbn: book for book in books}

    @classmethod
    def from_records(cls, records: Iterable[dict]) -> "Library":
        return cls(Book(**record) for record in records)

    def add(self, book: Book) -> None:
        self._books[book.isbn] = book

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self) -> Iterator[Book]:
        yield from self._books.values()

    def __contains__(self, isbn: object) -> bool:
        return isbn in self._books

    def __str__(self) -> str:
        return f"Knihovna: {len(self)} knih, {len(self.available_books)} k dispozici"

    @property
    def available_books(self) -> list[Book]:
        return [book for book in self if book.available]

    def by_author(self, author: str) -> Iterator[Book]:
        return (book for book in self if book.author == author)

    def borrow(self, isbn: str, member: Member) -> bool:
        book = self._books.get(isbn)
        if book is None or not book.available or not member.can_borrow():
            return False
        book.available = False
        member.borrowed.append(book)
        return True

    def return_book(self, isbn: str, member: Member) -> bool:
        book = self._books.get(isbn)
        if book is None or book not in member.borrowed:
            return False
        book.available = True
        member.borrowed.remove(book)
        return True


lib = Library.from_records(RECORDS)
anna = Member("Anna")
petr = Member("Petr", max_books=5)

print(lib, len(lib), "111" in lib)
print([str(b) for b in lib.by_author("Karel Čapek")])
print(anna.max_books, petr.max_books, Member.max_books)  # 2 5 2
print(lib.borrow("111", anna), lib.borrow("111", petr))  # True False
print(lib.borrow("222", anna), lib.borrow("333", anna))  # True False
print(lib)  # Knihovna: 4 knih, 2 k dispozici
print(lib.return_book("111", petr), lib.return_book("111", anna))  # False True
print(lib.borrow("333", anna), lib.borrow("111", petr), lib.borrow("444", petr))
print(lib, lib.available_books)  # Knihovna: 4 knih, 0 k dispozici []
print(min(lib, key=lambda b: b.year))
print(Library())  # Knihovna: 0 knih, 0 k dispozici

from collections import Counter
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
            self.max_books = max_books

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

    def __getitem__(self, isbn: str) -> Book:
        return self._books[isbn]  # KeyError probublá z dictu

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

    def count_by_author(self) -> dict[str, int]:
        return dict(Counter(book.author for book in self))

    def oldest_available(self) -> Book | None:
        return min(self.available_books, key=lambda book: book.year, default=None)

    def stats(self) -> dict[str, int]:
        available = len(self.available_books)
        return {"total": len(self), "available": available, "borrowed": len(self) - available}


lib2 = Library.from_records(RECORDS)
print(lib2["333"])  # Saturnin (Zdeněk Jirotka, 1942)
print(lib2.count_by_author(), Library().count_by_author())
print(lib2.stats(), lib2.oldest_available())
lib2.borrow("444", Member("Eva"))
print(lib2.oldest_available(), lib2.stats())  # R.U.R. …, borrowed 1
print(Library().oldest_available())  # None
lib2["999"]  # KeyError: '999'

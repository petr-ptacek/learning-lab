from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Generator

RECORDS = [
    {"isbn": "111", "title": "R.U.R.", "author": "Karel Čapek", "year": 1920},
    {"isbn": "222", "title": "Krakatit", "author": "Karel Čapek", "year": 1924},
    {"isbn": "333", "title": "Saturnin", "author": "Zdeněk Jirotka", "year": 1942},
    {"isbn": "444", "title": "Babička", "author": "Božena Němcová", "year": 1855},
]


@dataclass(kw_only=True)
class Book:
    isbn: str
    title: str
    author: str
    year: int
    available: bool = field(default=True)

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"


class Member:
    max_books = 2

    def __init__(self, name: str, max_books: int | None = None) -> None:
        self.name = name
        self.borrowed: list[Book] = []

        if max_books is not None:
            self.max_books = max_books

    @property
    def can_borrow(self) -> bool:
        return len(self.borrowed) < self.max_books


class Library:
    def __init__(self, books: list[Book] | None = None) -> None:
        self.books: dict[str, Book] = {book.isbn: book for book in books or []}

    @classmethod
    def from_records(cls, records: list):
        return cls([Book(**data) for data in records])

    @property
    def available_books(self) -> list[Book]:
        return [book for book in self.books.values() if book.available]

    def by_author(self, author: str):
        for book in self.books.values():
            if book.author == author:
                yield book

    def add(self, book: Book):
        self.books[book.isbn] = book

    def borrow(self, isbn: str, member: Member) -> bool:
        book = self.books.get(isbn, None)

        if not (
            book
            and book.available
            and book not in member.borrowed
            and member.can_borrow
        ):
            return False

        book.available = False
        member.borrowed.append(book)

        return True

    def return_book(self, isbn: str, member: Member) -> bool:
        book = self.books.get(isbn, None)

        if not (book and book in member.borrowed):
            return False

        book.available = True
        member.borrowed.remove(book)

        return True

    def count_by_author(self):
        counts = defaultdict(int)

        for book in self.books.values():
            counts[book.author] += 1

        return dict(counts)

    def oldest_available(self):
        return min(
            (book for book in self.available_books),
            key=lambda book: book.year,
            default=None,
        )

    def stats(self):
        total = len(self)
        borrowed = len([book for book in self.books.values() if book.available])
        available = len(self.available_books)

        stats = {
            "total": total,
            "borrowed": borrowed,
            "available": available,
        }

        return stats

    def __contains__(self, isbn: str) -> bool:
        return isbn in self.books

    def __iter__(self):
        yield from self.books.values()

    def __len__(self):
        return len(self.books)

    def __str__(self) -> str:
        return (
            f"Knihovna: {len(self.books)} knih, {len(self.available_books)} k dispozici"
        )

    def __getitem__(self, isbn: str) -> Book:
        try:
            return self.books[isbn]
        except KeyError:
            raise KeyError(f"No such book: {isbn}")


lib = Library.from_records(RECORDS)
anna = Member("Anna")
petr = Member("Petr", max_books=5)

print(str(lib))
print(lib.count_by_author())

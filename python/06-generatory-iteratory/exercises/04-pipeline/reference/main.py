from collections.abc import Iterable, Iterator

LOG = """\
2026-10-01 08:00:01 INFO server started
2026-10-01 08:05:12 WARN disk usage 85%

2026-10-01 08:07:44 ERROR db timeout
# ručně přidaná poznámka
2026-10-01 09:12:03 INFO user anna logged in
2026-10-01 09:15:30 ERROR payment failed

2026-10-01 10:00:00 INFO backup done
2026-10-01 10:30:00 ERROR backup verification failed
"""

type Record = tuple[str, str, str]


def lines(text: str) -> Iterator[str]:
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield line


def parse(lines: Iterable[str]) -> Iterator[Record]:
    for line in lines:
        _, time, level, message = line.split(maxsplit=3)
        yield time, level, message


def with_level(records: Iterable[Record], level: str) -> Iterator[Record]:
    return (record for record in records if record[1] == level)


def messages(records: Iterable[Record]) -> Iterator[str]:
    return (message for _, _, message in records)


def count_by_level(records: Iterable[Record]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for _, level, _ in records:
        counts[level] = counts.get(level, 0) + 1
    return counts


# next(with_level(parse(lines(LOG)), "ERROR")) přečte jen 3 řádky:
# INFO a WARN with_level zahodí, u ERROR má výsledek a všechny
# generátory se zastaví na svém yield. Zbytek logu nikdo nečte.

print(list(messages(with_level(parse(lines(LOG)), "ERROR"))))
print(list(messages(with_level(parse(lines(LOG)), "DEBUG"))))
print(next(parse(lines(LOG))))
print(len(list(lines(LOG))))
print(list(lines("")))
print(list(lines("# jen komentář\n\n")))
print(count_by_level(parse(lines(LOG))))
print(count_by_level(parse(lines(""))))

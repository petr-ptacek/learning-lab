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


def errors_per_hour(records: Iterable[Record]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for time, _, _ in with_level(records, "ERROR"):
        hour = time[:2]
        counts[hour] = counts.get(hour, 0) + 1
    return counts


def count(iterable: Iterable[object]) -> int:
    return sum(1 for _ in iterable)


# len(list(gen)) nejdřív uloží všechny prvky do paměti, jen aby je
# spočítal. sum(1 for _ in gen) drží v paměti jen průběžný součet.

print(errors_per_hour(parse(lines(LOG))))
print(errors_per_hour([]))
print(count(lines(LOG)))
print(count(x for x in range(10) if x % 3 == 0))
print(count([]))

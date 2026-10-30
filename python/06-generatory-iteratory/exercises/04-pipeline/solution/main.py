from collections.abc import Iterable

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


def lines(text: str):
    for l in text.splitlines():
        stripped = l.strip()

        if stripped.startswith("#") or stripped == "":
            continue

        print("čtu: ", stripped)
        yield stripped


def parse(lines: Iterable):
    for l in lines:
        temp = l.split(None, 3)
        time = temp[1]
        severity = temp[2]
        message = temp[3]

        yield time, severity, message


def count_by_level(records: Iterable):
    result = dict()

    for r in records:
        severity = r[1]
        result[severity] = result.get(severity, 0) + 1

    return result


def with_level(records: Iterable, level):
    return (r for r in records if r[1] == level)


def messages(records: Iterable):
    return (r[2] for r in records)


print(next(with_level(parse(lines(LOG)), "ERROR")))
# print(list(messages(with_level(parse(lines(LOG)), "ERROR"))))

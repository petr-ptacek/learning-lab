def split_time(seconds):
    """
    Split the seconds into hours, minutes and seconds.
    :param seconds:
    :return:
    """

    hours = seconds // (60 * 60)
    minutes = (seconds - (hours * 60 * 60)) // 60
    _seconds = seconds - ((hours * 60 * 60) + (minutes * 60))

    return hours, minutes, _seconds


def format_time(seconds):
    """
    Format seconds into HH:MM:SS format.
    :param seconds:
    :return:
    """

    h, m, s = split_time(abs(seconds))

    sign = "-" if seconds < 0 else ""
    hours = f"{h}"
    minutes = f"{m:02d}"
    seconds = f"{s:02d}"

    return f"{sign}{hours}:{minutes}:{seconds}"


def print_table(func, start, end, *, step=1, width=8):
    """
    Print a table between start and end and show the result from func.
    """

    if end < start:
        return

    print(f"{f"x":>{width}}|{f"func(x)":>{width}}")
    for i in range(start, end + 1, step):
        t = func(i)

        print(f"{f"{i}":>{width}}|{f"{t}":>{width}}")


def split_time_test_raw():
    cases = [
        3661,
        0,
        59,
        3600,
        86399,
        90061
    ]

    print(f"{"seconds":12}|{"split_time(seconds)":24}")
    print("-" * 36)
    for case in cases:
        h, m, s = split_time(case)
        print(f"{f"{case}":12}|{f"({h}, {m}, {s})":12}")


def main():
    # print(split_time.__doc__)
    #
    # print("\n")
    #
    # print_table(
    #     lambda x: pow(x, 2),
    #     1,
    #     5,
    #     width=24
    # )
    #
    # print("\n")
    #
    # print_table(
    #     format_time,
    #     0,
    #     7200,
    #     step=1800
    # )

    print(format_time(-6))


main()

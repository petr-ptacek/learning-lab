def split_time(seconds):
    """Split seconds into hours, minutes and seconds."""
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    return hours, minutes, seconds % 60


def format_time(seconds):
    """Return seconds formatted as H:MM:SS, with a leading - if negative."""
    sign = "-" if seconds < 0 else ""
    hours, minutes, secs = split_time(-seconds if seconds < 0 else seconds)
    return f"{sign}{hours}:{minutes:02}:{secs:02}"


def print_table(func, start, end, *, step=1, width=8):
    """Print x | func(x) for x from start to end inclusive."""
    for x in range(start, end + 1, step):
        print(f"{x:>{width}} | {func(x):>{width}}")


print(split_time.__doc__)
print_table(lambda x: x ** 2, 1, 5)
print_table(format_time, -3600, 3600, step=1800)
print_table(lambda x: x * 10, -2, 2, width=4)

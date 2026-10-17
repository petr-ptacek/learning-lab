def split_time(seconds):
    """Split seconds into hours, minutes and seconds."""
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    return hours, minutes, seconds % 60


def format_time(seconds):
    """Return seconds formatted as H:MM:SS."""
    hours, minutes, secs = split_time(seconds)
    return f"{hours}:{minutes:02}:{secs:02}"


def print_table(func, start, end, *, step=1):
    """Print x | func(x) for x from start to end inclusive."""
    for x in range(start, end + 1, step):
        print(f"{x:>8} | {func(x):>8}")


print(split_time.__doc__)
print_table(lambda x: x ** 2, 1, 5)
print_table(format_time, 0, 7200, step=1800)

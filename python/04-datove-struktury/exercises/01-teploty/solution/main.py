def print_stats(temps: list[float], days: list[str]) -> None:
    if not temps:
        print("No temps")
        return

    first_item = temps[0]
    last_item = temps[-1]
    count = len(temps)

    min_item = temps[0]
    min_item_idx = 0

    max_item = temps[0]
    max_item_idx = 0

    summary = 0

    for idx in range(len(temps)):
        temp = temps[idx]

        if temp < min_item:
            min_item = temp
            min_item_idx = idx

        if temp > max_item:
            max_item = temp
            max_item_idx = idx

        summary += temp

    avg = round(summary / count, 2)
    above_avg_count = 0

    for temp in temps:
        if temp > avg:
            above_avg_count += 1

    print(f"First item: {first_item}")
    print(f"Last item: {last_item}")
    print(f"Last 2 items: {temps[-2:]}")
    print(f"Measurements count: {count}")
    print(f"Min: {min_item}, Max: {max_item}, Avg: {avg}")
    print(f"Above avg: {above_avg_count}")
    print(f"Hottest day: {days[max_item_idx]}")
    print(f"Frostest day: {days[min_item_idx]}")


print_stats(
    [12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5],
    ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
)

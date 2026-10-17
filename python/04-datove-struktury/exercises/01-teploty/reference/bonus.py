def print_stats(temps, days):
    if len(temps) == 0:
        print("Žádná data")
        return

    lowest_i = highest_i = 0
    total = 0
    for i in range(len(temps)):
        if temps[i] < temps[lowest_i]:
            lowest_i = i
        if temps[i] > temps[highest_i]:
            highest_i = i
        total += temps[i]
    average = total / len(temps)

    above = 0
    for temp in temps:
        if temp > average:
            above += 1

    print(f"První: {temps[0]}, poslední: {temps[-1]}")
    print(f"Poslední dvě: {temps[-2:]}")
    print(f"Počet měření: {len(temps)}")
    print(f"Min: {temps[lowest_i]}, max: {temps[highest_i]}, průměr: {average:.2f}")
    print(f"Nad průměrem: {above}")
    print(f"Nejtepleji: {days[highest_i]}, nejchladněji: {days[lowest_i]}")


for temps, days in [
    ([12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5], ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]),
    ([20.0, 20.0], ["So", "Ne"]),
    ([-3.0, -1.5, -7.0], ["Po", "Út", "St"]),
    ([], []),
]:
    print_stats(temps, days)
    print()

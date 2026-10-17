def print_stats(temps):
    if len(temps) == 0:
        print("Žádná data")
        return

    lowest = highest = temps[0]
    total = 0
    for temp in temps:
        if temp < lowest:
            lowest = temp
        if temp > highest:
            highest = temp
        total += temp
    average = total / len(temps)

    above = 0
    for temp in temps:
        if temp > average:
            above += 1

    print(f"První: {temps[0]}, poslední: {temps[-1]}")
    print(f"Poslední dvě: {temps[-2:]}")
    print(f"Počet měření: {len(temps)}")
    print(f"Min: {lowest}, max: {highest}, průměr: {average:.2f}")
    print(f"Nad průměrem: {above}")


for temps in [
    [12.5, 15.0, 9.5, 18.0, 14.5, 11.0, 16.5],
    [5.0],
    [-3.0, -1.5, -7.0],
    [20.0, 20.0],
    [],
]:
    print_stats(temps)
    print()

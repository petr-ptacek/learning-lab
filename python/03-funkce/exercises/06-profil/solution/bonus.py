def print_profile(**info):
    infos_count = len(info)

    for key, value in info.items():
        print(f'{key}: {value}', end='; ')

    print(f"Pocet udaju {infos_count}")


print_profile(name="Petr", age=30)
print_profile(city="Brno", occupation="programator", age=30)
print_profile()

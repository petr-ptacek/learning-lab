def print_profile(**info):
    for key in info:
        print(f"{key}: {info[key]}")


def data_count(**info):
    return len(info)


print_profile(name="Petr", age=30)
print(f"Počet údajů: {data_count(name='Petr', age=30)}")

print_profile(city="Brno", occupation="programátor", age=25)
print(f"Počet údajů: {data_count(city='Brno', occupation='programátor', age=25)}")

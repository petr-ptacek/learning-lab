def print_profile(**info):
    for key, value in info.items():
        print(f'{key}: {value}')


print_profile(name="Petr", age=30)
print_profile(city="Brno", occupation="programator", age=30)
print_profile()

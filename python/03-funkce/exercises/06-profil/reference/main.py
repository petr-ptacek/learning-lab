def print_profile(**info):
    for key in info:
        print(f"{key}: {info[key]}")


print_profile(name="Petr", age=30)
print_profile(city="Brno", occupation="programátor", age=25)
print_profile()

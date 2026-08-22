def greet(name, greeting="Hello", exclamation_count=1):
    return f"{greeting}, {name}{'!' * exclamation_count}"


name = input("Enter your name: ")
greeting = input("Enter your greeting: ")
exclamation_count = int(input("Enter your exclamation count: ") or '1')

if greeting:
    print(greet(name, greeting, exclamation_count=exclamation_count))
else:
    print(greet(name, exclamation_count=exclamation_count))

def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


name = input("Enter your name: ")
greeting = input("Enter your greeting: ")

if greeting:
    print(greet(name, greeting))
else:
    print(greet(name))

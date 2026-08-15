CURRENT_YEAR = 2026

name = input("Jak se jmenuješ? ")
age = int(input("Kolik ti je let? "))
city = input("Kde bydlíš? ")
birth_year = CURRENT_YEAR - age

paper = f"""
{'-' * 4} Vizitka {'-' * 4} 
Jméno: {name}
Věk: {age}
Město: {city}
Rok narozeni {{{birth_year}}}
"""

print(paper)

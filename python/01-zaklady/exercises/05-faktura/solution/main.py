unit_a = input("Polozka: ")
value_a = float(input("Cena: "))
amount_a = int(input("Kusu: "))
summary_a = value_a * amount_a

unit_b = input("Polozka: ")
value_b = float(input("Cena: "))
amount_b = int(input("Kusu: "))
summary_b = value_b * amount_b

unit_c = input("Polozka: ")
value_c = float(input("Cena: "))
amount_c = int(input("Kusu: "))
summary_c = value_c * amount_c

summary_all = summary_a + summary_b + summary_c

discount = int(input("Sleva %: "))
discount_value = summary_all * (discount / 100)

total = summary_all - discount_value

paper = f"""
--- Faktura ---
{'Polozka':15}{'Ks':>10} {'Cena/ks':15}{'Celkem':>15}
{unit_a:15}{amount_a:>10} {value_a:15,.2f}{summary_a:>15,.2f}
{unit_b:15}{amount_b:>10} {value_b:15,.2f}{summary_b:>15,.2f}
{unit_c:15}{amount_c:>10} {value_c:15,.2f}{summary_c:>15,.2f}
{'-'*60}
{'Mezisoucet:':25} {summary_all:>30,.2f}
{f'Sleva ({discount}%):':25} {discount_value:>30,.2f}
{'Celkem k uhrade:':25} {total:>30,.2f}
"""

print(paper)

unit = input("Název položky: ")
value = float(input("Cena za kus bez DPH (desetinné číslo): "))
amount = int(input("Počet kusů (celé číslo): "))

value_no_dph = value * amount
dph = value_no_dph * 0.21
value_result = value_no_dph + dph

paper = f"""
--- Účtenka ---
{'Položka:':<15}{unit:>10}
{'Počet (ks):':<15}{amount:>10}
{'Cena bez DPH:':<15}{value_no_dph:>10.2f}
{'DPH (21%):':<15}{dph:>10.2f}
{'Celkem:':<15}{value_result:>10.2f}
"""

print(paper)

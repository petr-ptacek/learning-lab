subject_a = input("Nazev predmetu: ")
mark_a = int(input("Známka predmetu: "))

subject_b = input("Nazev predmetu: ")
mark_b = int(input("Známka predmetu: "))

subject_c = input("Nazev predmetu: ")
mark_c = int(input("Známka predmetu: "))

mark_average = (mark_a + mark_b + mark_c) / 3

row_header = f"{'Predmet':15}{'Známka':>15}"
row_a = f"{subject_a:15}{mark_a:>15}"
row_b = f"{subject_b:15}{mark_b:>15}"
row_c = f"{subject_c:15}{mark_c:>15}"
row_average = f"{'Prumer:':15}{mark_average:>15.2f}"

separator_length = max(len(row_header), len(row_a), len(row_b), len(row_c), len(row_average))
row_separator = "-" * separator_length

paper = f"""
{'Vysvedceni':-^{separator_length}}
{row_header}
{row_a}
{row_b}
{row_c}
{row_separator}
{row_average}
"""

print(paper)

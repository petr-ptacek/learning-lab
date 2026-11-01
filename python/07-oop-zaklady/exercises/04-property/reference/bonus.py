from functools import cached_property


class Report:
    def __init__(self, numbers: list[float]) -> None:
        self.numbers = numbers

    @cached_property
    def total(self) -> float:
        print("počítám…")
        return sum(self.numbers)

    @property
    def average(self) -> float:
        if not self.numbers:
            return 0
        return round(self.total / len(self.numbers), 2)


r = Report([10, 20, 30, 45])
print(r.total)  # počítám… 105
print(r.total)  # 105 (z cache)
print(r.average)  # 26.25
r.numbers.append(100)
# 105: hodnota leží ve vars(r)["total"] a instance má při hledání
# přednost před třídou, takže se metoda vůbec nezavolá. V pořádku pro
# data, která se nemění (Django instance na jeden request), chyba pro
# měnitelná data.
print(r.total)
del r.total  # smaže záznam z instance, odkryje se metoda na třídě
print(r.total)  # počítám… 205

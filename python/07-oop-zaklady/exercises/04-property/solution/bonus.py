from functools import cached_property


class Report:
    def __init__(self, numbers: list[int]):
        self.numbers = numbers

    @cached_property
    def total(self):
        print("pocitam...")
        return sum(self.numbers)

    @property
    def average(self):
        if not self.numbers:
            return 0

        return round(self.total / len(self.numbers), 2)


r = Report([10, 20, 30, 45])
print(r.total)
# Pocitam 105
print(r.total)
# 105

print(r.average)
# 105/4
r.numbers.append(100)

print(r.total)
# nezmeneno 105

del r.total
print(vars(r))

print(r.total)
# pocitam, 205
print(vars(r))

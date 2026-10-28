def apply_all(functions, value):
    return list(map(lambda function: function(value), functions))


print(apply_all([abs, str, lambda x: x * 2], -3))
print(apply_all([], 5))

# None místo funkce = nech jen truthy prvky, stejné jako filter(bool, ...).
# [0] je neprázdný seznam, takže truthy; [] je prázdný, takže falsy.
print(list(filter(None, ["", "a", 0, 1, None, [], [0]])))

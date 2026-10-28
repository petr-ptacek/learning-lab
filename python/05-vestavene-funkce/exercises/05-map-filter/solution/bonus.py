def apply_all(functions, value):
    return list(map(lambda f: f(value), functions))


print(apply_all([abs, str, lambda x: x * 2], -3))
print(apply_all([], 5))

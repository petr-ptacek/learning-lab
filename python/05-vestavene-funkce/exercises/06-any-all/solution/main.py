def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False

    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_no_space = all(not char.isspace() for char in password)

    return has_digit and has_upper and has_no_space


for case in ("Heslo123", "HESLOHESLO1", "heslo123", "Heslohes", "Heslo1", "Hes lo123"):
    print(f"{case}: {is_valid_password(case)}")


def all_passed(scores, limit=50):
    return all(score >= limit for score in scores)


print(all_passed([80, 65, 90, 50]))


def any_failed(scores, limit=50):
    return any(score < limit for score in scores)


print(any_failed([80, 65, 90, 45]))

# all_passed([]) vrací True
# protoze tam neni zadny item, co by nesplnoval podminku

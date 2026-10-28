def is_valid_password(password):
    return (
        len(password) >= 8
        and any(char.isdigit() for char in password)
        and any(char.isupper() for char in password)
        and not any(char.isspace() for char in password)
    )


def all_passed(scores, limit=50):
    return all(score >= limit for score in scores)


def any_failed(scores, limit=50):
    return any(score < limit for score in scores)


for password in ["Heslo123", "HESLOHESLO1", "heslo123", "Heslohes", "Heslo1", "Hes lo123"]:
    print(password, is_valid_password(password))

# all([]) je True: neexistuje prvek, který by podmínku porušil.
# any([]) je False: neexistuje prvek, který by ji splnil.
for scores in [[80, 65, 90], [80, 45, 90], [50], []]:
    print(scores, all_passed(scores), any_failed(scores))

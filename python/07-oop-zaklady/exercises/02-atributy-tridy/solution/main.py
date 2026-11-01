class Settings:
    language = "cs"
    tags = []


s1 = Settings()
# vytvori se instance Settings

s2 = Settings()
# vytvori se  instance Settings

s1.language = "en"
# vytvori se instancni promenna na s1

s1.tags.append("beta")
# mutuje se class promenna, vsechny instance maji ted tag beta

print(s1.language, s2.language, Settings.language)
# en, cs, cs

print(s2.tags)
# [beta]

print(vars(s1), vars(s2))
# __dict__ { language: "en" }, __dict__ {}

Settings.language = "de"
# prirazeni class promenne nd "de"

print(s1.language, s2.language)
# en - tady ma s1 instancni promennou, proto zastinuje class promennou, de

del s1.language
# odstraneni instancni promenne

print(s1.language)
# nyni class promenna "de"


class Ticket:
    next_id = 1
    priority = "normal"

    def __init__(self, title, priority=None):
        self.title = title
        if priority is not None:
            self.priority = priority
        self.id = Ticket.next_id
        Ticket.next_id += 1


class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)


cart = Cart()

print(vars(cart))

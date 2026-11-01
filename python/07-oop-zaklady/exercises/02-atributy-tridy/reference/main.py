class Settings:
    language = "cs"
    tags = []


s1 = Settings()
s2 = Settings()
s1.language = "en"  # přiřazení přes instanci → nový atribut na s1, zastíní třídu
s1.tags.append("beta")  # mutace: čtení najde seznam na třídě a změní ho
print(s1.language, s2.language, Settings.language)  # en cs cs
print(s2.tags)  # ['beta'] (seznam je jen jeden, sdílený)
print(vars(s1), vars(s2))  # {'language': 'en'} {}

Settings.language = "de"  # přiřazení na třídě → vidí ho všichni bez vlastní hodnoty
print(s1.language, s2.language)  # en de

del s1.language  # smaže atribut instance, odkryje se třída
print(s1.language)  # de


class Ticket:
    next_id = 1
    priority = "normal"

    def __init__(self, title: str, priority: str | None = None) -> None:
        self.id = Ticket.next_id
        Ticket.next_id += 1
        self.title = title
        if priority is not None:
            self.priority = priority


class Cart:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, item: str) -> None:
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)


t1 = Ticket("Nejde přihlášení")
t2 = Ticket("Pomalý web", "high")
t3 = Ticket("Překlep v patičce")
print(t1.id, t2.id, t3.id, Ticket.next_id)  # 1 2 3 4
print(vars(t1))  # {'id': 1, 'title': 'Nejde přihlášení'}
print(vars(t2))  # {'id': 2, 'title': 'Pomalý web', 'priority': 'high'}
Ticket.priority = "low"
print(t1.priority, t2.priority)  # low high

c1, c2 = Cart(), Cart()
c1.add("mléko")
c1.add("chléb")
print(c1.items, c1.count(), c2.count())  # ['mléko', 'chléb'] 2 0

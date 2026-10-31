class Broken:
    def hello():
        return "ahoj"


Broken().hello()
# predava se 1 pozicni argument, ala metoda nema zadny parametr definovany, proto chyba, v runtime se tam predava dana isntance

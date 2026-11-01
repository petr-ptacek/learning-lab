from collections.abc import Iterable, Iterator


def format_seconds(total: int) -> str:
    minutes, seconds = divmod(total, 60)
    return f"{minutes}:{seconds:02d}"


class Song:
    def __init__(self, title: str, seconds: int) -> None:
        self.title = title
        self.seconds = seconds

    def __repr__(self) -> str:
        return f"Song({self.title!r}, {self.seconds!r})"

    @property
    def duration(self) -> str:
        return format_seconds(self.seconds)


class Playlist:
    def __init__(self, name: str, songs: Iterable[Song] = ()) -> None:
        self.name = name
        self.songs = list(songs)  # vždy nový seznam, ať nesdílíme ten volajícího

    def add(self, song: Song) -> None:
        self.songs.append(song)

    def __len__(self) -> int:
        return len(self.songs)

    def __iter__(self) -> Iterator[Song]:
        yield from self.songs

    def __getitem__(self, index):
        return self.songs[index]

    def __contains__(self, title: object) -> bool:
        return any(song.title == title for song in self.songs)

    @property
    def total_seconds(self) -> int:
        return sum(song.seconds for song in self.songs)

    @property
    def total_duration(self) -> str:
        return format_seconds(self.total_seconds)


p = Playlist("Ráno")
print(len(p), bool(p))  # 0 False: bez __bool__ Python použije __len__
p.add(Song("Imagine", 183))
# reversed bez __reversed__ použije __len__ + __getitem__ (indexy od konce)
print(len(p), bool(p), list(reversed(p)))  # 1 True [Song('Imagine', 183)]

p.add(Song("Bohemian Rhapsody", 354))
p.add(Song("Hey Jude", 431))
print("Imagine" in p, p[-1], p[:2])
print(p.total_seconds, p.total_duration)  # 968 16:08

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
        self.songs = list(songs)

    def add(self, song: Song) -> None:
        self.songs.append(song)

    def __len__(self) -> int:
        return len(self.songs)

    def __iter__(self) -> Iterator[Song]:
        yield from self.songs

    # p[:2] vrací list, protože jen delegujeme na list. Pro Playlist by
    # se musel slice rozlišit od indexu:
    #   if isinstance(index, slice):
    #       return Playlist(self.name, self.songs[index])
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

    def titles(self) -> list[str]:
        return [song.title for song in self.songs]

    def __add__(self, other: object) -> "Playlist":
        if not isinstance(other, Playlist):
            return NotImplemented
        return Playlist(f"{self.name} + {other.name}", self.songs + other.songs)

    def __repr__(self) -> str:
        return f"Playlist({self.name!r}, {len(self)} skladeb)"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Playlist):
            return NotImplemented
        return self.titles() == other.titles()


p = Playlist("Ráno", [Song("Bohemian Rhapsody", 354), Song("Imagine", 183), Song("Hey Jude", 431)])
q = Playlist("Večer", [Song("Yesterday", 125)])
print(p + q, (p + q).total_duration, len(p))  # Playlist('Ráno + Večer', 4 skladeb) 18:13 3
print(Playlist("A", [Song("X", 1)]) == Playlist("B", [Song("X", 1)]))  # True
print(Playlist("A", [Song("X", 1)]) == Playlist("A", [Song("Y", 1)]))  # False

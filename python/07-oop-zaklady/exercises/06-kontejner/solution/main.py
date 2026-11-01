from collections.abc import Iterable


class Song:
    def __init__(self, title: str, seconds: int):
        self.title = title
        self.seconds = seconds

    def __repr__(self):
        return f"Song({self.title!r}, {self.seconds})"

    @property
    def duration(self):
        minutes, seconds = divmod(self.seconds, 60)

        return f"{minutes}:{seconds:02d}"


class Playlist:
    def __init__(self, name: str, songs: Iterable["Song"] | None = None):
        self.name = name
        self.songs = list(songs or []).copy()

    def add(self, song: Song):
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        yield from self.songs

    def __getitem__(self, index):
        return self.songs[index]

    def __contains__(self, title):
        return any(title == song.title for song in self.songs)

    def __add__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented

        songs = self.songs + other.songs
        name = f"{self.name} + {other.name}"

        return Playlist(name, songs)

    def __repr__(self) -> str:
        return f"Playlist({self.name!r}, {len(self.songs)})"

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented

        return len(self.songs) == len(other.songs) and all(
            a.title == b.title for a, b in zip(self.songs, other.songs)
        )

    def clear(self):
        self.songs = []

    @property
    def total_seconds(self):
        return sum(song.seconds for song in self.songs)

    @property
    def total_duration(self):
        seconds = self.total_seconds
        minutes, seconds = divmod(seconds, 60)

        return f"{minutes}:{seconds:02d}"


song_1 = Song("Bohemian Rhapsody", 354)
song_2 = Song("Kratka", 59)
song_3 = Song("Nic", 0)
song_4 = Song("Presne", 120)

playlist_1 = Playlist("Best", [song_1, song_2, song_3])
playlist_2 = Playlist("Best", [song_1, song_2, song_3])

print(playlist_1 == playlist_2)

# playlist.clear()


# print(bool(playlist))
# print(playlist.total_duration)
# print("Nic" in playlist)
# print(playlist[2])
# print(len(playlist))

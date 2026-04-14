class LibraryItem:
    def __init__(self, name, artist, rating=0, image="", audio="", track_number=""):
        self.track_number = track_number
        self.name = name
        self.artist = artist
        self.rating = rating
        self.play_count = 0
        self.image = image
        self.audio = audio

    def info(self):
        return f"{self.name} - {self.artist} {self.stars()}"

    def stars(self):
        return "*" * self.rating
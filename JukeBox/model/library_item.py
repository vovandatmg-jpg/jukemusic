class LibraryItem:
    def __init__(self, name, artist, rating=0, image="", audio="", track_number="", play_count=0):
        self.name = name
        self.artist = artist
        self.rating = rating
        self.image = image
        self.audio = audio
        self.track_number = track_number
        self.play_count = play_count

    def info(self):
        return f"{self.name} - {self.artist} {self.stars()}"

    def stars(self):
        return "*" * self.rating

    def detail_text(self):
        return (
            f"Track Number: {self.track_number}\n"
            f"Track Name: {self.name}\n"
            f"Artist: {self.artist}\n"
            f"Rating: {self.stars()}\n"
            f"Play Count: {self.play_count}"
        )
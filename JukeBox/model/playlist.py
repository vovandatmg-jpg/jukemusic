from JukeBox.model.library_item import LibraryItem


class Playlist:
    def __init__(self):
        self.items: list[LibraryItem] = []

    def add_track(self, track: LibraryItem):
        if track is None:
            return False

        if self.contains(track.track_number):
            return False

        self.items.append(track)
        return True

    def contains(self, track_number: str):
        return any(item.track_number == track_number for item in self.items)

    def get_items(self):
        return list(self.items)

    def reset(self):
        self.items.clear()

    def is_empty(self):
        return len(self.items) == 0
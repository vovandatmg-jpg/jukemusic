import model.track_library as lib
from model.playlist import Playlist
from view.gui_utils import normalise_track_number


class PlaylistController:
    def __init__(self):
        self.playlist = Playlist()

    def get_playlist_text(self):
        lines = []

        for count, track in enumerate(self.playlist.get_items(), start=1):
            lines.append(
                f"{count}. {track.track_number} - {track.name} - {track.artist} - Play count: {track.play_count}"
            )

        return "\n".join(lines)

    def add_track(self, track_number_text):
        track_number, error = normalise_track_number(track_number_text)

        if error:
            return {
                "text": self.get_playlist_text(),
                "status": error,
                "ok": False
            }

        track = lib.get_item(track_number)
        if track is None:
            return {
                "text": self.get_playlist_text(),
                "status": "Track not found",
                "ok": False
            }

        if self.playlist.contains(track_number):
            return {
                "text": self.get_playlist_text(),
                "status": "Track already in playlist",
                "ok": False
            }

        self.playlist.add_track(track)

        return {
            "text": self.get_playlist_text(),
            "status": "Track added successfully",
            "ok": True
        }

    def play_playlist(self):
        if self.playlist.is_empty():
            return {
                "text": self.get_playlist_text(),
                "status": "Playlist is empty",
                "ok": False
            }

        for track in self.playlist.get_items():
            lib.increment_play_count(track.track_number, save=False)

        lib.save_changes()

        return {
            "text": self.get_playlist_text(),
            "status": "Playlist played successfully",
            "ok": True
        }

    def reset_playlist(self):
        self.playlist.reset()

        return {
            "text": "",
            "status": "Playlist reset",
            "ok": True
        }
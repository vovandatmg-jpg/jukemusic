import model.track_library as lib
from model.playlist import Playlist
from controller.input_validator import normalise_track_number


class PlaylistController:
    def __init__(self):
        self.playlist = Playlist()

    def get_playlist_items(self):
        return self.playlist.get_items()

    def get_playlist_text(self):
        lines = []

        for count, track in enumerate(self.playlist.get_items(), start=1):
            lines.append(
                f"{count}. {track.track_number} - {track.name} - {track.artist} - Play count: {track.play_count}"
            )

        return "\n".join(lines)

    def get_track_details_text(self, track_number):
        track = lib.get_item(track_number)
        return track.detail_text() if track else "Track not found"

    def get_audio_path(self, track_number):
        return lib.get_audio_path(track_number)

    def get_image_path(self, track_number):
        return lib.get_image_path(track_number)

    def register_play(self, track_number, save=True):
        lib.increment_play_count(track_number, save=save)
        return self.get_track_details_text(track_number)

    def save_changes(self):
        lib.save_changes()

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

        if not self.playlist.add_track(track):
            return {
                "text": self.get_playlist_text(),
                "status": "Track already in playlist",
                "ok": False
            }

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

        return {
            "text": self.get_playlist_text(),
            "status": "Playing playlist",
            "ok": True
        }

    def reset_playlist(self):
        self.playlist.reset()

        return {
            "text": "",
            "status": "Playlist reset",
            "ok": True
        }
import model.track_library as lib
from model.playlist import Playlist
from controller.input_validator import normalise_track_number


class PlaylistController:
    def __init__(self):
        self.playlist = Playlist()
        self.current_index = -1
        self.playing = False

    def get_playlist_items(self):
        return self.playlist.get_items()

    def get_playlist_text(self):
        items = self.playlist.get_items()

        if not items:
            return ""

        lines = []

        lines.append(
            f"{'No.':<5}{'Track':<8}{'Track Name':<28}{'Artist':<24}{'Play Count':<10}"
        )
        lines.append("-" * 78)

        for count, track in enumerate(items, start=1):
            lines.append(
                f"{count:<5}"
                f"{track.track_number:<8}"
                f"{track.name[:27]:<28}"
                f"{track.artist[:23]:<24}"
                f"{track.play_count:<10}"
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

    def add_track_to_playlist(self, track_number_text):
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
                "ok": False,
                "track": None
            }

        self.current_index = 0
        self.playing = True

        return {
            "text": self.get_playlist_text(),
            "status": "Playing playlist",
            "ok": True,
            "track": self.get_current_track()
        }

    def simulate_playlist_play(self):
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

    def get_current_track(self):
        items = self.playlist.get_items()

        if not self.playing:
            return None

        if self.current_index < 0 or self.current_index >= len(items):
            return None

        return items[self.current_index]

    def move_next_track(self):
        if not self.playing:
            return None

        self.current_index += 1
        items = self.playlist.get_items()

        if self.current_index >= len(items):
            self.playing = False
            self.current_index = -1
            return None

        return items[self.current_index]

    def stop_playlist(self):
        self.playing = False
        self.current_index = -1

    def is_playing(self):
        return self.playing

    def reset_playlist(self):
        self.stop_playlist()
        self.playlist.reset()

        return {
            "text": "",
            "status": "Playlist reset",
            "ok": True
        }
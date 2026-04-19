import model.track_library as lib
from controller.input_validator import normalise_track_number, validate_rating


class TrackController:
    def _format_track_list(self, items):
        return lib.format_items(items)

    def list_tracks(self):
        items = lib.get_all_items()

        return {
            "text": self._format_track_list(items),
            "status": "Tracks listed successfully",
            "ok": True
        }

    def get_artists(self):
        return lib.get_artists()

    def get_track_details_text(self, track_number):
        track = lib.get_item(track_number)
        return track.detail_text() if track else "Track not found"

    def view_track(self, track_number_text):
        track_number, error = normalise_track_number(track_number_text)

        if error:
            return {
                "success": False,
                "details": error,
                "status": "Invalid track number",
                "ok": False,
                "track_number": None,
                "image_path": None
            }

        track = lib.get_item(track_number)

        if track is None:
            return {
                "success": False,
                "details": f"Track {track_number} not found",
                "status": "Track not found",
                "ok": False,
                "track_number": None,
                "image_path": None
            }

        return {
            "success": True,
            "details": track.detail_text(),
            "status": "Track displayed successfully",
            "ok": True,
            "track_number": track_number,
            "image_path": lib.get_image_path(track_number)
        }

    def search_tracks(self, keyword):
        keyword = keyword.strip()

        if keyword == "":
            return {
                "text": "",
                "status": "Please enter a track name or artist",
                "ok": False
            }

        results = lib.search_tracks(keyword)

        if not results:
            return {
                "text": "No matching tracks found",
                "status": "No matching tracks found",
                "ok": False
            }

        return {
            "text": self._format_track_list(results),
            "status": "Search completed",
            "ok": True
        }

    def filter_tracks(self, artist_name):
        results = lib.filter_by_artist(artist_name)

        if not results:
            return {
                "text": "No tracks found for this artist",
                "status": "No tracks found for this artist",
                "ok": False
            }

        return {
            "text": self._format_track_list(results),
            "status": "Artist filter applied",
            "ok": True
        }

    def get_audio_path(self, track_number):
        return lib.get_audio_path(track_number)

    def register_play(self, track_number, save=True):
        lib.increment_play_count(track_number, save=save)
        return self.get_track_details_text(track_number)

    def update_rating(self, track_number_text, rating_text):
        track_number, track_error = normalise_track_number(track_number_text)
        new_rating, rating_error = validate_rating(rating_text)

        if track_error and rating_error:
            return {
                "text": f"{track_error}\n{rating_error}",
                "status": "Invalid track number and rating",
                "ok": False
            }

        if track_error:
            return {
                "text": track_error,
                "status": track_error,
                "ok": False
            }

        if rating_error:
            return {
                "text": rating_error,
                "status": rating_error,
                "ok": False
            }

        track = lib.get_item(track_number)

        if track is None:
            return {
                "text": "Track not found",
                "status": "Track not found",
                "ok": False
            }

        lib.set_rating(track_number, new_rating)

        updated_track = lib.get_item(track_number)

        return {
            "text": updated_track.detail_text(),
            "status": "Rating updated successfully",
            "ok": True
        }
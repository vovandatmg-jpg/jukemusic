import model.track_library as lib
from view.gui_utils import normalise_track_number


def validate_rating(rating_text):
    rating_text = rating_text.strip()

    if rating_text == "":
        return None, "Please enter a rating"

    if not rating_text.isdigit():
        return None, "Rating must be a number"

    rating = int(rating_text)

    if rating < 1 or rating > 5:
        return None, "Rating must be between 1 and 5"

    return rating, None


class TrackController:
    def list_tracks(self):
        return {
            "text": lib.list_all(),
            "status": "Tracks listed successfully",
            "ok": True
        }

    def get_artists(self):
        return lib.get_artists()

    def get_track_details_text(self, track_number):
        name = lib.get_name(track_number)
        artist = lib.get_artist(track_number)
        rating = lib.get_rating(track_number)
        play_count = lib.get_play_count(track_number)

        return (
            f"Track Number: {track_number}\n"
            f"Track Name: {name}\n"
            f"Artist: {artist}\n"
            f"Rating: {'*' * rating}\n"
            f"Play Count: {play_count}"
        )

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

        if lib.get_name(track_number) is None:
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
            "details": self.get_track_details_text(track_number),
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

        if results == "No matching tracks found":
            return {
                "text": results,
                "status": "No matching tracks found",
                "ok": False
            }

        return {
            "text": results,
            "status": "Search completed",
            "ok": True
        }

    def filter_tracks(self, artist_name):
        results = lib.filter_by_artist(artist_name)

        if results == "No tracks found for this artist":
            return {
                "text": results,
                "status": "No tracks found for this artist",
                "ok": False
            }

        return {
            "text": results,
            "status": "Artist filter applied",
            "ok": True
        }

    def get_audio_path(self, track_number):
        return lib.get_audio_path(track_number)

    def register_play(self, track_number):
        lib.increment_play_count(track_number)
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

        if lib.get_name(track_number) is None:
            return {
                "text": "Track not found",
                "status": "Track not found",
                "ok": False
            }

        lib.set_rating(track_number, new_rating)

        result = (
            f"Track number: {track_number}\n"
            f"Name: {lib.get_name(track_number)}\n"
            f"Artist: {lib.get_artist(track_number)}\n"
            f"New rating: {'*' * lib.get_rating(track_number)}\n"
            f"Play count: {lib.get_play_count(track_number)}\n"
        )

        return {
            "text": result,
            "status": "Rating updated successfully",
            "ok": True
        }
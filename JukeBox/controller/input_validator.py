def normalise_track_number(track_number):
    track_number = track_number.strip()

    if track_number == "":
        return None, "Please enter a track number"
    if not track_number.isdigit():
        return None, "Track number must be numeric"
    if len(track_number) > 2:
        return None, "Track number must be 1 or 2 digits"

    return track_number.zfill(2), None

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
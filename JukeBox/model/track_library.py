import csv
import os
from model.library_item import LibraryItem

library = {}
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FILE = os.path.join(BASE_DIR, "tracks.csv")
DEFAULT_IMAGE_FILE = os.path.join(BASE_DIR, "img", "default.png")


def resolve_file_path(path_text):
    if not path_text:
        return None

    if os.path.isabs(path_text):
        full_path = path_text
    else:
        full_path = os.path.normpath(os.path.join(BASE_DIR, path_text))

    return full_path if os.path.exists(full_path) else None


def get_all_items():
    return [library[key] for key in sorted(library.keys())]


def format_items(items):
    lines = []
    for item in items:
        lines.append(f"{item.track_number} {item.info()} plays:{item.play_count}")
    return "\n".join(lines)


def load_library():
    library.clear()

    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                track_number = row["track_number"].strip().zfill(2)
                name = row["name"].strip()
                artist = row["artist"].strip()
                rating = int(row["rating"])
                play_count = int(row["play_count"])
                image = row.get("image", "").strip()
                audio = row.get("audio", "").strip()

                item = LibraryItem(
                    name=name,
                    artist=artist,
                    rating=rating,
                    image=image,
                    audio=audio,
                    track_number=track_number,
                    play_count=play_count
                )
                library[track_number] = item

    except FileNotFoundError:
        print("tracks.csv not found")
    except KeyError as e:
        print(f"Missing column in CSV: {e}")
    except ValueError:
        print("Invalid number format in tracks.csv")


def save_library():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "track_number",
            "name",
            "artist",
            "rating",
            "play_count",
            "image",
            "audio"
        ])

        for item in get_all_items():
            writer.writerow([
                item.track_number,
                item.name,
                item.artist,
                item.rating,
                item.play_count,
                item.image,
                item.audio
            ])


def save_changes():
    save_library()


def get_item(key):
    return library.get(key)


def list_all():
    return format_items(get_all_items())


def get_name(key):
    item = get_item(key)
    return item.name if item else None


def get_artist(key):
    item = get_item(key)
    return item.artist if item else None


def get_rating(key):
    item = get_item(key)
    return item.rating if item else -1


def set_rating(key, rating):
    item = get_item(key)
    if item:
        item.rating = rating
        save_library()


def get_play_count(key):
    item = get_item(key)
    return item.play_count if item else -1


def increment_play_count(key, save=True):
    item = get_item(key)
    if item:
        item.play_count += 1
        if save:
            save_library()


def get_image(key):
    item = get_item(key)
    return item.image if item else None


def get_audio(key):
    item = get_item(key)
    return item.audio if item else ""


def get_image_path(key):
    image_path = resolve_file_path(get_image(key))
    if image_path:
        return image_path

    if os.path.exists(DEFAULT_IMAGE_FILE):
        return DEFAULT_IMAGE_FILE

    return None


def get_audio_path(key):
    return resolve_file_path(get_audio(key))


def search_tracks(keyword):
    keyword = keyword.strip().lower()

    if keyword == "":
        return []

    matches = []
    for item in get_all_items():
        if keyword in item.name.lower() or keyword in item.artist.lower():
            matches.append(item)

    return matches


def filter_by_artist(artist_name):
    artist_name = artist_name.strip().lower()

    if artist_name == "":
        return []

    matches = []
    for item in get_all_items():
        if item.artist.strip().lower() == artist_name:
            matches.append(item)

    return matches


def get_artists():
    return sorted({item.artist for item in library.values()})


load_library()
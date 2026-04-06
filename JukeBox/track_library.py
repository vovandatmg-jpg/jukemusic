import csv
import os
from library_item import LibraryItem

library = {}
CSV_FILE = os.path.join(os.path.dirname(__file__), "tracks.csv")


def load_library():
    library.clear()

    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                track_number = row["track_number"]
                name = row["name"]
                artist = row["artist"]
                rating = int(row["rating"])
                play_count = int(row["play_count"])
                image = row.get("image", "").strip()
                audio = row.get("audio", "").strip()

                item = LibraryItem(name, artist, rating, image, audio)
                item.play_count = play_count
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

        for key in sorted(library.keys()):
            item = library[key]
            writer.writerow([
                key,
                item.name,
                item.artist,
                item.rating,
                item.play_count,
                item.image,
                item.audio
            ])


def get_item(key):
    return library.get(key)


def list_all():
    lines = []

    for key in sorted(library.keys()):
        item = library[key]
        lines.append(f"{key} {item.info()} plays:{item.play_count}")

    return "\n".join(lines)


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


def save_changes():
    save_library()


def get_image(key):
    item = get_item(key)
    return item.image if item else None


def get_audio(key):
    item = get_item(key)
    return item.audio if item else ""


def get_image_path(key):
    image = get_image(key)

    if image:
        if os.path.isabs(image):
            image_path = image
        else:
            image_path = os.path.normpath(
                os.path.join(os.path.dirname(__file__), image)
            )

        if os.path.exists(image_path):
            return image_path

    default_path = os.path.join(os.path.dirname(__file__), "img", "default.png")
    if os.path.exists(default_path):
        return default_path

    return None


def get_audio_path(key):
    audio = get_audio(key)

    if audio:
        if os.path.isabs(audio):
            audio_path = audio
        else:
            audio_path = os.path.normpath(
                os.path.join(os.path.dirname(__file__), audio)
            )

        if os.path.exists(audio_path):
            return audio_path

    return None





def search_tracks(keyword):
    keyword = keyword.strip().lower()

    if keyword == "":
        return "Please enter a search keyword"

    lines = []

    for key in sorted(library.keys()):
        item = library[key]
        if keyword in item.name.lower() or keyword in item.artist.lower():
            lines.append(f"{key} {item.info()} plays:{item.play_count}")

    if not lines:
        return "No matching tracks found"

    return "\n".join(lines)


def filter_by_artist(artist_name):
    lines = []

    for key in sorted(library.keys()):
        item = library[key]
        if item.artist.strip().lower() == artist_name.strip().lower():
            lines.append(f"{key} {item.info()} plays:{item.play_count}")

    if not lines:
        return "No tracks found for this artist"

    return "\n".join(lines)


def get_artists():
    return sorted({item.artist for item in library.values()})


load_library()
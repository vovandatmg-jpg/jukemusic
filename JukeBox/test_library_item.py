from library_item import LibraryItem


def test_library_item_name():
    item = LibraryItem("Song A", "Artist A", 3)
    assert item.name == "Song A"


def test_library_item_artist():
    item = LibraryItem("Song B", "Artist B", 3)
    assert item.artist == "Artist B"


def test_library_item_rating():
    item = LibraryItem("Song C", "Artist C", 3)
    assert item.rating == 3


def test_stars():
    item = LibraryItem("Song A", "Artist A", 4)
    assert item.stars() == "****"


def test_library_item_play_count_default():
    item = LibraryItem("Song A", "Artist A", 3)
    assert item.play_count == 0


def test_library_item_image_default():
    item = LibraryItem("Song A", "Artist A", 3)
    assert item.image == ""


def test_library_item_audio_default():
    item = LibraryItem("Song A", "Artist A", 3)
    assert item.audio == ""


def test_library_item_image_value():
    item = LibraryItem("Song A", "Artist A", 3, "img/01.png")
    assert item.image == "img/01.png"


def test_library_item_audio_value():
    item = LibraryItem("Song A", "Artist A", 3, "img/01.png", "audio/01.mp3")
    assert item.audio == "audio/01.mp3"


def test_info():
    item = LibraryItem("Song A", "Artist A", 3)
    assert item.info() == "Song A - Artist A ***"
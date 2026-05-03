import model.track_library as lib
from controller.track_controller import TrackController


def get_first_track():
    items = lib.get_all_items()
    assert len(items) > 0
    return items[0]


def test_view_track_valid():
    controller = TrackController()
    track = get_first_track()

    result = controller.view_track(track.track_number)

    assert result["ok"] is True
    assert result["status"] == "Track displayed successfully"
    assert track.name in result["details"]


def test_view_track_invalid_text():
    controller = TrackController()

    result = controller.view_track("abc")

    assert result["ok"] is False
    assert result["status"] == "Invalid track number"
    assert result["details"] == "Track number must be numeric"


def test_search_tracks_empty():
    controller = TrackController()

    result = controller.search_tracks("")

    assert result["ok"] is False
    assert result["status"] == "Please enter a track name or artist"


def test_search_tracks_valid():
    controller = TrackController()
    track = get_first_track()
    keyword = track.name.split()[0]

    result = controller.search_tracks(keyword)

    assert result["ok"] is True
    assert result["status"] == "Search completed"
    assert track.name in result["text"]


def test_filter_tracks_valid_artist():
    controller = TrackController()
    track = get_first_track()

    result = controller.filter_tracks(track.artist)

    assert result["ok"] is True
    assert result["status"] == "Artist filter applied"
    assert track.artist in result["text"]


def test_update_rating_invalid_rating():
    controller = TrackController()
    track = get_first_track()

    result = controller.update_rating(track.track_number, "6")

    assert result["ok"] is False
    assert result["status"] == "Rating must be between 1 and 5"
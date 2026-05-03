import model.track_library as lib
from controller.playlist_controller import PlaylistController


def get_first_track_number():
    items = lib.get_all_items()
    assert len(items) > 0
    return items[0].track_number


def test_add_track_to_playlist_valid():
    controller = PlaylistController()
    track_number = get_first_track_number()

    result = controller.add_track_to_playlist(track_number)

    assert result["ok"] is True
    assert result["status"] == "Track added successfully"
    assert len(controller.get_playlist_items()) == 1


def test_add_track_to_playlist_invalid_text():
    controller = PlaylistController()

    result = controller.add_track_to_playlist("abc")

    assert result["ok"] is False
    assert result["status"] == "Track number must be numeric"


def test_add_duplicate_track_to_playlist():
    controller = PlaylistController()
    track_number = get_first_track_number()

    controller.add_track_to_playlist(track_number)
    result = controller.add_track_to_playlist(track_number)

    assert result["ok"] is False
    assert result["status"] == "Track already in playlist"
    assert len(controller.get_playlist_items()) == 1


def test_play_playlist_empty():
    controller = PlaylistController()

    result = controller.play_playlist()

    assert result["ok"] is False
    assert result["status"] == "Playlist is empty"


def test_reset_playlist():
    controller = PlaylistController()
    track_number = get_first_track_number()

    controller.add_track_to_playlist(track_number)
    result = controller.reset_playlist()

    assert result["ok"] is True
    assert result["status"] == "Playlist reset"
    assert controller.get_playlist_items() == []
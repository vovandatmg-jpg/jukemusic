from gui_utils import normalise_track_number


def test_normalise_track_number_empty():
    number, error = normalise_track_number("")
    assert number is None
    assert error == "Please enter a track number"


def test_normalise_track_number_text():
    number, error = normalise_track_number("abc")
    assert number is None
    assert error == "Track number must be numeric"


def test_normalise_track_number_too_long():
    number, error = normalise_track_number("123")
    assert number is None
    assert error == "Track number must be 1 or 2 digits"


def test_normalise_track_number_one_digit():
    number, error = normalise_track_number("4")
    assert number == "04"
    assert error is None


def test_normalise_track_number_two_digits():
    number, error = normalise_track_number("05")
    assert number == "05"
    assert error is None


def test_normalise_track_number_with_spaces():
    number, error = normalise_track_number(" 7 ")
    assert number == "07"
    assert error is None
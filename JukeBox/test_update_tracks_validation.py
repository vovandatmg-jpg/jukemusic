from update_tracks import validate_rating


def test_validate_rating_empty():
    rating, error = validate_rating("")
    assert rating is None
    assert error == "Please enter a rating"


def test_validate_rating_text():
    rating, error = validate_rating("abc")
    assert rating is None
    assert error == "Rating must be a number"


def test_validate_rating_too_low():
    rating, error = validate_rating("0")
    assert rating is None
    assert error == "Rating must be between 1 and 5"


def test_validate_rating_too_high():
    rating, error = validate_rating("6")
    assert rating is None
    assert error == "Rating must be between 1 and 5"


def test_validate_rating_valid_middle():
    rating, error = validate_rating("3")
    assert rating == 3
    assert error is None


def test_validate_rating_with_spaces():
    rating, error = validate_rating(" 5 ")
    assert rating == 5
    assert error is None
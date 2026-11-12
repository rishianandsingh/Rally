from datetime import date, timedelta

from validation import EventInput, validate_event

FUTURE = date.today() + timedelta(days=7)


def test_valid_event_has_no_errors() -> None:
    assert validate_event(EventInput("Hackathon", "desc", 3, FUTURE)) == []


def test_empty_title_rejected() -> None:
    assert "Title is required." in validate_event(EventInput("  ", "desc", 3, FUTURE))


def test_past_date_rejected() -> None:
    past = date.today() - timedelta(days=1)
    assert "Event date cannot be in the past." in validate_event(EventInput("X", "d", 3, past))
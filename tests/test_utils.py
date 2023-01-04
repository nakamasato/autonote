from datetime import date, datetime

from autonote.utils import get_first_monday


def test_get_first_monday_jan():
    d = date(2023, 1, 1)
    monday = get_first_monday(d)
    assert datetime(2023, 1, 2) == monday


def test_get_first_monday_feb():
    d = date(2023, 2, 1)
    monday = get_first_monday(d)
    assert datetime(2023, 2, 6) == monday


def test_get_first_monday_mar():
    d = date(2023, 3, 1)
    monday = get_first_monday(d)
    assert datetime(2023, 3, 6) == monday

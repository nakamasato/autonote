from datetime import date

from autonote.utils import get_first_monday, get_next_weekday


def test_get_first_monday_jan():
    d = date(2023, 1, 1)
    monday = get_first_monday(d)
    assert date(2023, 1, 2) == monday


def test_get_first_monday_feb():
    d = date(2023, 2, 1)
    monday = get_first_monday(d)
    assert date(2023, 2, 6) == monday


def test_get_first_monday_mar():
    d = date(2023, 3, 1)
    monday = get_first_monday(d)
    assert date(2023, 3, 6) == monday


def test_get_next_weekday():
    d = date(2023, 3, 1)
    monday = get_next_weekday(d, 0)
    assert date(2023, 3, 6) == monday

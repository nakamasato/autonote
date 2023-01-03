from datetime import datetime, timedelta


def get_first_monday(d):
    day_7 = datetime(d.year, d.month, 7)
    offset = -day_7.weekday()  # weekday = 0 means monday
    return day_7 + timedelta(offset)

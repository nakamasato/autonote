from datetime import date, timedelta


def get_first_monday(d):
    """Get first Monday of the month."""
    day_7 = date(d.year, d.month, 7)
    offset = -day_7.weekday()  # weekday = 0 means monday
    return day_7 + timedelta(offset)


def get_next_weekday(d, weekday):
    """Get next weekday.
    For example, you can get next monday by next_weekday(d, 0)
    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

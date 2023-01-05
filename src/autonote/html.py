from datetime import datetime, timedelta
from enum import Enum

from jinja2 import Environment, PackageLoader

from .utils import get_first_monday

Period = Enum("Period", ["QUARTERLY", "MONTHLY", "WEEKLY", "DAILY"])


def generate(d=None, date_format="%Y/%m/%d"):
    if d is None:
        d = datetime.today()
    monday = get_first_monday(d)
    first_day_of_next_month = (d.replace(day=1) + timedelta(days=32)).replace(day=1)
    weeks = []
    while monday < first_day_of_next_month:
        friday = monday + timedelta(days=4)
        weeks.append(
            {
                "start_date": monday.strftime(date_format),
                "end_date": friday.strftime(date_format),
            }
        )
        monday += timedelta(weeks=1)

    data = {
        "title": "title",
        "weeks": weeks,
    }
    env = Environment(loader=PackageLoader("autonote", "templates"))
    template = env.get_template("monthly_report.html.tpl")
    return template.render(data)


def read(filename):
    with open(filename, "r") as file:
        data = file.read().rstrip()
    return data


if __name__ == "__main__":
    print(generate())

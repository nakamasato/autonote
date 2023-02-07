from datetime import date, timedelta
from os import environ, path

from jinja2 import Environment, FileSystemLoader

from autonote.confluence import ConfluenceClient

data = {
    "weeks": [
        {
            "start_date": "2023/02/06",
            "end_date": "2023/02/10",
        },
        {
            "start_date": "2023/02/20",
            "end_date": "2023/02/24",
        },
        {
            "start_date": "2023/02/07",
            "end_date": "2023/03/03",
        },
    ]
}
env = Environment(loader=FileSystemLoader(path.dirname(__file__)))
template = env.get_template("templates/monthly_report.html.tpl")
content = template.render(data)
client = ConfluenceClient()
client.create_page(
    parent_page_id=environ["CONFLUENCE_PARENT_PAGE_ID"],
    title=f"2023/02/07 Feb test",
    body=content,
)

# Examples

## 1. Confluence

### 1.1. Create a confluence page

Currently only support pre-defined page. TODO: make it configurable

1. Set environment variables:

    ```
    export CONFLUENCE_URL=https://xxx.atlassian.net
    export CONFLUENCE_USERNAME=<yourname>@domain.com
    export CONFLUENCE_PASSWORD=<TOKEN>
    ```
1. Prepare `templates/monthly_report.html.tpl`
    ```html
    <html>

    <head>
    	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    	<title></title>
    </head>

    <body>
    	<article>
    		<div>
    			{% for week in weeks %}
    			<h1>{{ week.start_date }}~{{week.end_date}}</h1>
    			<ul>
    				<li></li>
    			</ul>
    			{% endfor %}
    			<h1>KPT</h1>
    			<ul>
    				<li>K</li>
    				<li>P</li>
    				<li>T</li>
    			</ul>
    		</div>
    	</article>
    </body>

    </html>
    ```
1. Run
    ```python
    from os import path, environ
    from datetime import date, timedelta

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
    ```

    <details><summary>generate data with code</summary>

    ```python
    def prepare_data():
        date_format = "%Y/%m/%d"
        d = date.today()
        monday = date(2023, 2, 6)
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

        return {
            "weeks": weeks,
        }
    ```

    </details>

    Generated Page:

    <table><tr><td>
    <img src="../docs/confluence_page_0.png" width="200px" />
    </td></tr></table>

## 2. Notion

Prerequisite: Set environemnt variable

```
export NOTION_INTEGRATION_TOKEN=xxx
```

### 2.1. Create a Notion page

```python
from autonote.notion import NotionClient

client = NotionClient()
client.create_page(
    parent_page_id="<parent_page_id>",
    title="title",
    body="body",
    override=True, # update if exists
)
```

Generated page:

<table><tr><td>
<img src="../docs/notion_page_0.png" width="200px" />
</td></tr></table>


### 2.2. Create Notion database page from a template

```python
from autonote.notion import NotionClient

client = NotionClient()
client.create_page_from_template(
    template_id="<template_id>",
    title="OKR 2023Q1",
    override=True,
)
```

Template page:

<table><tr><td>
<img src="../docs/notion_template_page_0.png" width="200px" />
</td></tr></table>

Generated page:

<table><tr><td>
<img src="../docs/notion_page_1.png" width="200px" />
</td></tr></table>

## 2.3. Create Notion page from a template with dynamic values

```python
from autonote.notion import NotionClient

client = NotionClient()
kwargs={"Date": {"start": "2023-01-01", "end": "2023-03-31"}}
client.create_page_from_template(
    template_id="<template_id>",
    title="OKR 2023Q1",
    override=True,
    **kwargs
)
```

<table><tr><td>
<img src="../docs/notion_page_2.png" width="200px" />
</td></tr></table>

## 2.3. Create Notion page from a template with dynamic values

```python
from autonote.notion import NotionClient

client = NotionClient()
kwargs={"Date": {"start": "2023-01-01", "end": "2023-03-31"}}
client.create_page_from_template(
    template_id="<template_id>",
    title="OKR 2023Q1",
    override=True,
    **kwargs
)
```

<table><tr><td>
<img src="../docs/notion_page_2.png" width="200px" />
</td></tr></table>

## 2.3. Create Notion page from a template with dynamic values (properties)

```python
from autonote.notion import NotionClient

client = NotionClient()
kwargs={"Date": {"start": "2023-01-01", "end": "2023-03-31"}}
client.create_page_from_template(
    template_id="<template_id>",
    title="OKR 2023Q1",
    override=True,
    **kwargs
)
```

<table><tr><td>
<img src="../docs/notion_page_2.png" width="200px" />
</td></tr></table>

```
poetry run python examples/create_notion_page_from_template.py
```

## 2.4. Create Notion page from a templae with dynamic values (content)

```python
from autonote.notion import NotionClient

client = NotionClient()

kwargs = {
    "Date": {"start": "2023-02-04", "end": "2023-02-10"},
    "replace_rules": [
        {
            "block_types": ["heading_1"],  # target blocks to apply replacement
            "replace_str": "YYYY/MM/DD",  # replacement string match
            "replace_type": "datetime",  # currently only support "datetime"
            "date_format": "%Y/%m/%d",  # used to parse `start_date` and generate string from datetime when interpolating
            "start_date": "2023/02/04",  # start date
            "increment": True,  # if true, increment 1 day every time replacement is executed
        },
    ],
}
client.create_page_from_template(
    template_id="a7cc4f73460c4b9fa82be8d4ed74d8ca",
    title="weekly note",
    override=True,
    **kwargs
)
```

Template:

<table><tr><td>
<img src="../docs/notion_template_page_1.png" width="200px" />
</td></tr></table>

Generated page:

<table><tr><td>
<img src="../docs/notion_page_3.png" width="200px" />
</td></tr></table>

```bash
poetry run python examples/create_notion_page_from_template_with_value.py # start date & end date inserted
```

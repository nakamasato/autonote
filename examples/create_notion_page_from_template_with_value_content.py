from autonote.notion import NotionClient

client = NotionClient()

kwargs = {
    "Date": {"start": "2023-02-04", "end": "2023-02-10"},
    "URL": "https://www.google.com/",
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

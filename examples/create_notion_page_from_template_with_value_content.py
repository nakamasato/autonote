from autonote.notion import NotionClient

client = NotionClient()

kwargs = {
    "Date": {"start": "2023-02-04", "end": "2023-02-10"},
    "replace_rules": [
        {
            "block_types": ["heading_1"],
            "replace_str": "YYYY/MM/DD",
            "replace_type": "datetime",
            "date_format": "%Y/%m/%d",
            "start_date": "2023/02/04",
            "increment": True,
        },
    ],
}
client.create_page_from_template(
    template_id="a7cc4f73460c4b9fa82be8d4ed74d8ca",
    title="weekly note",
    override=True,
    **kwargs
)

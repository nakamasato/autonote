from autonote.notion import NotionClient

client = NotionClient()

kwargs = {"Start & End Date": {"start": "2023-01-01", "end": "2023-03-31"}}
client.create_page_from_template(template_id="ffbf0ff4a80047fa84fa741ad8bcfbe9", title="OKR 2023Q1", override=True, **kwargs)

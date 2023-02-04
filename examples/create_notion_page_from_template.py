from autonote.notion import NotionClient

client = NotionClient()

client.create_page_from_template(
    template_id="ffbf0ff4a80047fa84fa741ad8bcfbe9",
    title="OKR template",
    override=True,
)

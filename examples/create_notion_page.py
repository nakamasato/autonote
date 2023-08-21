from autonote.notion import NotionClient

client = NotionClient()
client.create_page(
    parent_page_id="8fdd653fdaf6498db09acfff88c9582d",
    title="title",
    body="body",
    override=True,
)

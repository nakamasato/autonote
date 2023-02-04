from autonote.notion import NotionClient

client = NotionClient()
client.create_page(
    parent_page_id="5d98fac8f41d4801b3c337be70dabba1",
    title="title",
    body="body",
    override=True,
)

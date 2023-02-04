from autonote.confluence import ConfluenceClient
from autonote.html import generate

content = generate()
client = ConfluenceClient()
client.create_page(
    "<confluence_parent_page_id>",
    title="title",
    body=content,
)

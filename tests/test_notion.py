from autonote.notion import NotionPage


def test_notion_page_simple_database():
    page = NotionPage(title="test title", body="test body")
    kwargs = page.database_content(parent_database_id="parent_database_id")
    assert kwargs["parent"] == {
        "type": "database_id",
        "database_id": "parent_database_id",
    }
    assert kwargs["properties"] == {
        "title": [{"type": "text", "text": {"content": "test title"}}]
    }
    assert kwargs["contents"] == [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "test body"}}]
            },
        },
    ]


def test_notion_page_with_properties():
    properties = {
        "Tags": {
            "id": "FQLU",
            "type": "multi_select",
            "multi_select": [
                {
                    "id": "f385f958-c732-4b78-986b-4ec5146c0fa6",
                    "name": "OKR",
                    "color": "green",
                }
            ],
        },
    }
    page = NotionPage(title="test title", body="test body")
    page.update_properties(properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Tags": [{"name": "OKR"}],
    }

    page = NotionPage(title="test title", body="test body", properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Tags": [{"name": "OKR"}],
    }


def test_notion_page_cannot_update_title():
    properties = {
        "Name": {
            "id": "title",
            "type": "title",
            "title": [{"type": "text", "text": {"content": "OKR template"}}],
        }
    }
    page = NotionPage(title="test title", body="test body")
    page.update_properties(properties=properties)
    assert page.properties["title"] == [
        {"type": "text", "text": {"content": "test title"}}
    ]

    page = NotionPage(title="test title", body="test body", properties=properties)
    assert page.properties["title"] == [
        {"type": "text", "text": {"content": "test title"}}
    ]

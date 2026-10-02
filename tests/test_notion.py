from unittest.mock import Mock

import pytest

from autonote.notion import NOTION_API_VERSION, NotionClient, NotionPage, NotionPageContent


def test_notion_page_parent_type():
    with pytest.raises(ValueError):
        NotionPage(title="test", parent_type="invalid")


def test_notion_page_simple_database():
    page = NotionPage(title="test title", parent_type="database_id")
    kwargs = page.pages_kwargs(parent_id="parent_database_id")
    assert kwargs == {
        "parent": {
            "type": "database_id",
            "database_id": "parent_database_id",
        },
        "properties": {"title": [{"type": "text", "text": {"content": "test title"}}]},
    }


def test_notion_page_data_source_parent():
    page = NotionPage(title="test title", parent_type="data_source_id")
    assert page.pages_kwargs(parent_id="source-id")["parent"] == {
        "type": "data_source_id",
        "data_source_id": "source-id",
    }


def test_notion_client_uses_latest_api_version(monkeypatch):
    token = "test-token"
    monkeypatch.setenv("NOTION_INTEGRATION_TOKEN", token)
    sdk_client = Mock()
    monkeypatch.setattr("autonote.notion.Client", sdk_client)

    NotionClient()

    sdk_client.assert_called_once_with(auth=token, notion_version=NOTION_API_VERSION)


def test_notion_page_with_properties_tag():
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
    page = NotionPage(title="test title", parent_type="page_id")
    page.update_properties(properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Tags": [
            {
                "id": "f385f958-c732-4b78-986b-4ec5146c0fa6",
                "name": "OKR",
                "color": "green",
            }
        ],
    }

    page = NotionPage(title="test title", parent_type="page_id", properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Tags": [
            {
                "id": "f385f958-c732-4b78-986b-4ec5146c0fa6",
                "name": "OKR",
                "color": "green",
            }
        ],
    }


def test_notion_page_with_properties_date():
    properties = {
        "Start Date": {
            "id": "k%3A%7Bd",
            "type": "date",
            "date": {"start": "2023-02-04", "end": "2023-02-10", "time_zone": None},
        }
    }
    page = NotionPage(title="test title", parent_type="page_id")
    page.update_properties(properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Start Date": {"start": "2023-02-04", "end": "2023-02-10", "time_zone": None},
    }

    page = NotionPage(title="test title", parent_type="page_id", properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Start Date": {"start": "2023-02-04", "end": "2023-02-10", "time_zone": None},
    }


def test_notion_page_with_properties_select():
    properties = {
        "Size": {
            "id": "qyqF",
            "type": "select",
            "select": {
                "id": "59a6cc39-cbe3-4cac-a013-6928a3b0705b",
                "name": "small",
                "color": "pink",
            },
        }
    }
    page = NotionPage(title="test title", parent_type="page_id", properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Size": {
            "id": "59a6cc39-cbe3-4cac-a013-6928a3b0705b",
            "name": "small",
            "color": "pink",
        },
    }


def test_notion_page_with_properties_empty():
    properties = {
        "Start Date": {
            "id": "k%3A%7Bd",
            "type": "date",
            "date": None,
        }
    }
    page = NotionPage(title="test title", parent_type="page_id")
    page.update_properties(properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Start Date": None,
    }

    page = NotionPage(title="test title", parent_type="page_id", properties=properties)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
        "Start Date": None,
    }


def test_notion_page_cannot_update_title():
    properties = {
        "Name": {
            "id": "title",
            "type": "title",
            "title": [{"type": "text", "text": {"content": "OKR template"}}],
        }
    }
    page = NotionPage(title="test title", parent_type="page_id")
    page.update_properties(properties=properties)
    assert page.properties["title"] == [{"type": "text", "text": {"content": "test title"}}]

    page = NotionPage(title="test title", parent_type="page_id", properties=properties)
    assert page.properties["title"] == [{"type": "text", "text": {"content": "test title"}}]


def test_notion_page_update_template_property_with_value_date():
    properties = {
        "Start Date": {
            "id": "k%3A%7Bd",
            "type": "date",
            "date": {"start": None, "end": None, "time_zone": None},
        }
    }
    kwargs = {"Start Date": {"start": "2023-02-04", "end": "2023-02-10"}}
    page = NotionPage(title="test", parent_type="page_id", properties=properties, **kwargs)
    assert page.properties["Start Date"] == {
        "start": "2023-02-04",
        "end": "2023-02-10",
        "time_zone": None,
    }


def test_notion_page_update_none_template_property_with_value_date():
    properties = {
        "Start Date": {
            "id": "k%3A%7Bd",
            "type": "date",
            "date": None,
        }
    }
    kwargs = {"Start Date": {"start": "2023-02-04", "end": "2023-02-10"}}
    page = NotionPage(title="test", parent_type="page_id", properties=properties, **kwargs)
    assert page.properties["Start Date"] == {"start": "2023-02-04", "end": "2023-02-10"}


def test_notion_page_update_none_template_property_with_value_url():
    properties = {
        "Start Date": {
            "id": "k%3A%7Bd",
            "type": "date",
            "date": None,
        },
        "URL": {"id": "TR%5C%5B", "type": "url", "url": None},
    }
    kwargs = {
        "Start Date": {"start": "2023-02-04", "end": "2023-02-10"},
        "URL": "https://www.google.com/",
    }
    page = NotionPage(title="test", parent_type="page_id", properties=properties, **kwargs)
    assert page.properties["URL"] == "https://www.google.com/"


def test_notion_page_update_template_property_with_nonexisting_value():
    kwargs = {"nonexisting key": {"start": "2023-02-04", "end": "2023-02-10"}}
    page = NotionPage(title="test title", parent_type="page_id", **kwargs)
    assert page.properties == {
        "title": [{"type": "text", "text": {"content": "test title"}}],
    }


def test_notion_page_content_from_body():
    content = NotionPageContent("body")
    assert content.contents == [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "body"}}]},
        }
    ]


def test_notion_page_content_update_contents():
    contents = [
        {"type": "table_of_contents", "table_of_contents": {"color": "gray"}},
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "YYYY/MM/DD (月)", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "YYYY/MM/DD (月)",
                        "href": None,
                    }
                ],
                "is_toggleable": False,
                "color": "default",
            },
        },
        {
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [], "color": "default"},
        },
        {"type": "paragraph", "paragraph": {"rich_text": [], "color": "default"}},
    ]
    content = NotionPageContent("body", contents=contents)
    assert content.contents == contents


def test_notion_page_content_update_contents_replace_datetime():
    contents = [
        {"type": "table_of_contents", "table_of_contents": {"color": "gray"}},
        {
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [], "color": "default"},
        },
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "YYYY/MM/DD (月)", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "YYYY/MM/DD (月)",
                        "href": None,
                    }
                ],
                "is_toggleable": False,
                "color": "default",
            },
        },
    ]
    replace_rules = [
        {
            "replace_type": "datetime",
            "block_types": "heading_1",
            "replace_str": "YYYY/MM/DD",
            "date_format": "%Y-%m-%d",
            "start_date": "2023-01-01",
        }
    ]
    content = NotionPageContent("body", contents=contents, replace_rules=replace_rules)
    assert content.contents[2]["heading_1"]["rich_text"][0]["text"]["content"] == "2023-01-01 (月)"
    assert content.contents[2]["heading_1"]["rich_text"][0]["plain_text"] == "2023-01-01 (月)"


def test_write_block_omits_null_optional_fields():
    block = {
        "type": "paragraph",
        "paragraph": {
            "icon": None,
            "rich_text": [{"type": "text", "text": {"content": "Example", "link": None}, "plain_text": "Example", "href": None}],
        },
    }

    assert NotionPageContent.as_write_block(block) == {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Example"}}]},
    }


def test_create_page_from_template_uses_data_source_and_writable_blocks():
    client = NotionClient.__new__(NotionClient)
    client.client = Mock()
    client.client.pages.retrieve.return_value = {
        "parent": {"type": "data_source_id", "data_source_id": "source-id"},
        "properties": {"Name": {"type": "title", "title": []}},
    }
    client.client.data_sources.query.return_value = {"results": []}
    client.client.pages.create.return_value = {"id": "new-page"}
    heading = {
        "object": "block",
        "id": "heading-id",
        "parent": {"type": "page_id", "page_id": "template-id"},
        "archived": False,
        "in_trash": False,
        "has_children": False,
        "type": "heading_1",
        "heading_1": {"rich_text": [{"type": "text", "text": {"content": "Hello"}, "plain_text": "Hello", "href": None}]},
    }
    list_item = {
        "object": "block",
        "id": "list-id",
        "has_children": True,
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": []},
    }
    child = {
        "object": "block",
        "id": "child-id",
        "has_children": False,
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Nested"}, "plain_text": "Nested"}]},
    }

    def list_blocks(block_id, **kwargs):
        if block_id == "template-id" and not kwargs:
            return {"results": [heading], "has_more": True, "next_cursor": "next"}
        if block_id == "template-id" and kwargs == {"start_cursor": "next"}:
            return {"results": [list_item], "has_more": False}
        if block_id == "list-id":
            return {"results": [child], "has_more": False}
        raise AssertionError((block_id, kwargs))

    client.client.blocks.children.list.side_effect = list_blocks
    result = client.create_page_from_template("template-id", "New page")

    assert result == {"id": "new-page"}
    client.client.data_sources.query.assert_called_once_with(data_source_id="source-id", filter={"property": "title", "title": {"equals": "New page"}})
    create_kwargs = client.client.pages.create.call_args.kwargs
    assert create_kwargs["parent"] == {"type": "data_source_id", "data_source_id": "source-id"}
    assert create_kwargs["children"] == [
        {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "Hello"}}]}},
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [],
                "children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Nested"}}]}}],
            },
        },
    ]
    client.client.blocks.children.append.assert_not_called()


def test_update_contents_keeps_old_blocks_if_append_fails():
    client = NotionClient.__new__(NotionClient)
    client.client = Mock()
    client.client.blocks.children.list.return_value = {
        "results": [{"id": "existing-id", "has_children": False, "type": "paragraph", "paragraph": {"rich_text": []}}],
        "has_more": False,
    }
    client.client.blocks.children.append.side_effect = RuntimeError("append failed")

    with pytest.raises(RuntimeError, match="append failed"):
        client.update_contents("page-id", [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": []}}])

    client.client.blocks.delete.assert_not_called()

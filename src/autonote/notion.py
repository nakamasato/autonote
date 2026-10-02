import argparse
import os
from copy import deepcopy
from datetime import datetime, timedelta

from notion_client import Client

NOTION_API_VERSION = "2026-03-11"
MAX_CHILDREN_PER_REQUEST = 100


class NotionMock:
    def create_page(self, parent_page_id, title, body):
        print(f"{parent_page_id=}, {title=}, {body=}")
        return {"id": "random_id"}


class NotionPage:
    """NotionPage contains parent and properties"""

    def __init__(self, title: str, parent_type: str, properties: dict | None = None, **kwargs) -> None:
        """Initialize NotionPage.

        Args:
            title(str): required to determine Notion page by title
            parent_type(str): one of 'data_source_id', 'database_id', or 'page_id'
            properties(dict): Notion property item. https://developers.notion.com/reference/property-item-object
        """
        self.title = title
        if parent_type not in {"data_source_id", "database_id", "page_id"}:
            raise ValueError("parent_type must be one of 'data_source_id', 'database_id', or 'page_id'")
        self.parent_type = parent_type
        self.properties = {
            "title": [
                {
                    "type": "text",
                    "text": {"content": self.title},
                }
            ]
        }
        if properties is not None:
            self.update_properties(properties, **kwargs)

    def pages_kwargs(self, parent_id: str) -> dict:
        return {
            "parent": {
                "type": self.parent_type,
                self.parent_type: parent_id,
            },
            "properties": self.properties,
        }

    def update_properties(self, properties: dict, **kwargs) -> None:
        """Update properties
        Example properties obtain from database page:
        {'Start Date': {'id': '%3CAfZ', 'type': 'date', 'date': None},
        'Tags': {'id': 'FQLU', 'type': 'multi_select', 'multi_select': [{'id': 'f385f958-c732-4b78-986b-4ec5146c0fa6', 'name': 'OKR', 'color': 'green'}]},
        'End Date': {'id': 'Vemz', 'type': 'date', 'date': None},
        'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': ...

        properties to set:
            {
                "Tags": [{"name": "OKR"}, {"name": "Test"}],
                "Start Date" : {"start": "2023-02-01"}, # An ISO 8601 format date, with optional time.
                "End Date" : {"start": "2023-02-10"}, # An ISO 8601 format date, with optional time.
            }
        """
        for k, v in properties.items():
            # skip title
            if v["type"] in {  # uneditable
                "title",
                "created_by",
                "last_edited_by",
                "last_edited_time",
                "created_time",
                "formula",
            }:
                continue
            else:
                # TODO: this might not work for some data type.
                self.properties[k] = v[v["type"]]
                print(f"update property {k}: {v[v['type']]}")

        # update value from kwargs
        for k, v in kwargs.items():
            if k in self.properties:
                if self.properties[k] is None:
                    self.properties[k] = v
                else:
                    self.properties[k].update(v)
                print(f"update property with value ({v}). new: {k}: {self.properties[k]}")
            else:
                print(f"{k} is not in properties")


class NotionPageContent:
    def __init__(self, body=None, contents=None, **kwargs):
        self.contents = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": body}}]},
            },
        ]
        if contents is not None:
            self.update_contents(contents, **kwargs)

    def update_contents(self, contents: dict, **kwargs) -> None:
        """Update contents with contents and **kwargs

        Args:
            contents (list): list of dict that contains type and the value e.g.
                {'type': 'table_of_contents', 'table_of_contents': {'color': 'gray'}}
                blocks that are returned from blocks.children.list["result"]
            kwargs (dict): you can pass replacement rule for the content.

        Example of contents:
        [{'type': 'table_of_contents', 'table_of_contents': {'color': 'gray'}}
        {'type': 'heading_1', 'heading_1': {'rich_text': [{'type': 'text', 'text':...
        {'type': 'numbered_list_item', 'numbered_list_item': {'rich_text': [], 'color': 'default'}}
        {'type': 'paragraph', 'paragraph': {'rich_text': [], 'color': 'default'}}]
        """
        self.contents = contents
        for e in self.contents:
            print(e)

        # update value from replace_rules
        SUPPORTED_REPLACE_TYPES = ["datetime"]
        for rule in kwargs.get("replace_rules", []):
            if rule.get("replace_type") not in SUPPORTED_REPLACE_TYPES:
                raise ValueError("'replace_type' is must be 'datetime'.")
            replace_type = rule.pop("replace_type")
            if replace_type == "datetime":
                self.update_contents_by_datetime(**rule)

    def update_contents_by_datetime(self, block_types, replace_str, date_format, start_date, increment=False):
        """Update contents with specified start_date
        Args:
            block_types (list): block types e.g. ["heading_1", "heading_2"]
            replace_str (str): the target string to replace
            date_format (str): date format e.g. '%Y/%m/%d'
            start_date (str): start date in the format of 'date_format'. e.g. '2023/02/04'
            increment (bool): true if increment during replacement
        """

        SUPPORTED_BLOCK_TYPES = [
            "heading_1",
            "heading_2",
            "heading_3",
        ]
        start_dt = datetime.strptime(start_date, date_format)  # noqa: DTZ007 - date-only template text
        dt = start_dt
        for blk in self.contents:
            if blk["type"] not in SUPPORTED_BLOCK_TYPES:
                continue
            if blk["type"] in block_types:
                str_before = blk[blk["type"]]["rich_text"][0]["plain_text"]
                blk[blk["type"]]["rich_text"][0]["text"]["content"] = blk[blk["type"]]["rich_text"][0]["text"]["content"].replace(
                    replace_str,
                    dt.strftime(date_format),
                )
                blk[blk["type"]]["rich_text"][0]["plain_text"] = blk[blk["type"]]["rich_text"][0]["plain_text"].replace(
                    replace_str,
                    dt.strftime(date_format),
                )
                str_after = blk[blk["type"]]["rich_text"][0]["plain_text"]
                print(f"updating contents type: {blk['type']}, {str_before=}, {str_after=}")
                if increment is True:
                    dt += timedelta(days=1)

    @staticmethod
    def _without_null_fields(value):
        """Omit unset response fields from block creation requests."""
        if isinstance(value, dict):
            return {key: NotionPageContent._without_null_fields(item) for key, item in value.items() if item is not None}
        if isinstance(value, list):
            return [NotionPageContent._without_null_fields(item) for item in value]
        return value

    @staticmethod
    def as_write_block(block: dict) -> dict:
        """Keep block content while removing fields returned only by read requests."""
        block_type = block["type"]
        data = deepcopy(block[block_type])
        for key in ("rich_text", "caption"):
            if key in data:
                data[key] = [{field: value for field, value in item.items() if field not in {"plain_text", "href"}} for item in data[key]]
        if "children" in data:
            data["children"] = [NotionPageContent.as_write_block(child) for child in data["children"]]
        return {"object": "block", "type": block_type, block_type: NotionPageContent._without_null_fields(data)}


class NotionClient:
    def __init__(self):
        self.client = Client(auth=os.environ["NOTION_INTEGRATION_TOKEN"], notion_version=NOTION_API_VERSION)

    def create_page(self, parent_page_id, title, body, override=False):
        """Create or update page.
        If there already exists pages with the given title,
        update the one with the latest last_edited_time.
        """
        pages_kwargs = NotionPage(title=title, parent_type="page_id").pages_kwargs(
            parent_id=parent_page_id,
        )
        content = NotionPageContent(body=body)
        pages = self.search_pages(query=title)
        if len(pages) == 0 or override is False:
            res = self.client.pages.create(**pages_kwargs, children=content.contents)
            print(f"page created successfully (id: {res['id']})")
        else:
            page_id = pages[0]["id"]  # update the first matched page
            res = self.client.pages.update(page_id, **pages_kwargs)
            print(f"page updated successfully (id: {page_id})")
            self.update_contents(page_id=page_id, contents=content.contents)
        return {"id": res["id"]}

    def create_page_from_template(self, template_id, title, override=False, **kwargs):
        """Create a new page from the given template_id.
        if override is True and there's a page with the same title, update the existing page.
        You can pass values of properties via kwargs
        """

        # Prepare NotionPage and NotionPageContent from template
        tpl = self.get_page(page_id=template_id)
        parent = tpl["parent"]
        if parent["type"] == "data_source_id":
            data_source_id = parent["data_source_id"]
        elif parent["type"] == "database_id":
            data_source_id = self._single_data_source_id(parent["database_id"])
        else:
            raise ValueError(f"The given template_id {template_id} is not a database template.")
        pages_kwargs = NotionPage(  # only properties
            title=title,
            parent_type="data_source_id",
            properties=tpl["properties"],
            **kwargs,  # update properties
        ).pages_kwargs(parent_id=data_source_id)
        # To get contents of a page, Retrieve block children
        # https://developers.notion.com/reference/get-block-children
        content = NotionPageContent(contents=self._template_blocks(template_id), **kwargs)
        children = [content.as_write_block(block) for block in content.contents]
        if len(children) > MAX_CHILDREN_PER_REQUEST:
            raise ValueError("A template with more than 100 top-level blocks is not supported")

        # Create or update a page
        res = self.get_data_source(
            data_source_id=data_source_id,
            filter={"property": "title", "title": {"equals": title}},
        )
        if len(res["results"]) == 0 or override is False:
            print(f"create a new page under data_source_id: {data_source_id}")
            res = self.client.pages.create(**pages_kwargs, children=children)
        else:
            page_id = res["results"][0]["id"]
            print(f"page with title '{title}' already exists (id: {page_id})")
            res = self.client.pages.update(page_id, **pages_kwargs)  # only update properties
            self.update_contents(page_id=page_id, contents=children)

        return res

    def search_pages(self, query: str) -> list:
        res = self.client.search(
            query=query,
            sort={  # TODO: enable to specify
                "direction": "descending",
                "timestamp": "last_edited_time",
            },
        ).get("results")
        print(f"found {len(res)} pages matching with query '{query}'")
        if len(res) == 0:
            return []
        return res

    def get_page(self, page_id: str) -> dict:
        """Retrieve a page.
        Endpoint documentation: https://developers.notion.com/reference/retrieve-a-page
        """
        return self.client.pages.retrieve(page_id=page_id)

    def get_database(self, database_id: str, **kwargs) -> dict:
        """Query the only data source in a database."""
        return self.get_data_source(self._single_data_source_id(database_id), **kwargs)

    def get_data_source(self, data_source_id: str, **kwargs) -> dict:
        """Query a data source for its pages."""
        return self.client.data_sources.query(data_source_id=data_source_id, **kwargs)

    def _single_data_source_id(self, database_id: str) -> str:
        data_sources = self.client.databases.retrieve(database_id=database_id)["data_sources"]
        if len(data_sources) != 1:
            raise ValueError("The database must have exactly one data source; use a data source template")
        return data_sources[0]["id"]

    def _all_child_blocks(self, block_id: str) -> list[dict]:
        """Read every page of direct child blocks."""
        blocks = []
        cursor = None
        while True:
            kwargs = {"start_cursor": cursor} if cursor else {}
            response = self.get_child_blocks(block_id=block_id, **kwargs)
            blocks.extend(response["results"])
            if not response.get("has_more"):
                break
            cursor = response["next_cursor"]
        return blocks

    def _template_blocks(self, block_id: str, depth: int = 0) -> list[dict]:
        """Read template blocks, including nested content."""
        blocks = self._all_child_blocks(block_id)
        for block in blocks:
            if block.get("has_children"):
                if depth >= 1:
                    raise ValueError("Templates with blocks nested more than two levels are not supported")
                block[block["type"]]["children"] = self._template_blocks(block["id"], depth + 1)
        return blocks

    def get_child_blocks(self, block_id: str, **kwargs) -> dict:
        """Get children blocks.
        You can pass page_id to get the contents of a page.
        """
        return self.client.blocks.children.list(block_id, **kwargs)

    def update_contents(self, page_id: str, contents: dict):
        """Update a page with the given contents."""
        existing = self._all_child_blocks(page_id)
        print(f"{len(existing)} blocks exist in page '{page_id}'")
        if len(contents) > MAX_CHILDREN_PER_REQUEST:
            raise ValueError("More than 100 top-level blocks are not supported")
        if contents:
            self.client.blocks.children.append(block_id=page_id, children=contents)
        for i, block in enumerate(existing):
            print(f"delete existing block {i} (block_id: {block['id']})")
            self.client.blocks.delete(block_id=block["id"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Notion page")
    parser.add_argument(
        "--notion_database_id",
        dest="notion_database_id",
        required=True,
        help="Notion database id under which new notion page will be created.",
    )
    parser.add_argument(
        "--dryrun",
        help="dryrun will not actually do the operation",
        action="store_true",
    )
    args = parser.parse_args()
    print(args)

    client = NotionMock() if args.dryrun else NotionClient()
    res = client.create_page(
        args.notion_database_id,
        title="title",
        body="body",
    )
    print(res)

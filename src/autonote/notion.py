import argparse
import os
from datetime import datetime, timedelta

from notion_client import Client


class NotionMock:
    def create_page(self, parent_page_id, title, body):
        print(f"{parent_page_id=}, {title=}, {body=}")
        return {"id": "random_id"}


class NotionPage:
    """NotionPage contains parent and properties"""

    def __init__(
        self, title: str, parent_type: str, properties: dict = None, **kwargs
    ) -> None:
        """Initialize NotionPage.

        Args:
            title(str): required to determine Notion page by title
            parent_type(str): one of 'database_id' or 'page_id'
            properties(dict): Notion property item. https://developers.notion.com/reference/property-item-object
        """
        self.title = title
        if parent_type not in {"database_id", "page_id"}:
            raise ValueError("parent_type must be one of 'database_id' or 'page_id'")
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
            if v["type"] == "title":
                continue
            elif v["type"] in {  # uneditable
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
                print(
                    f"update property with value ({v}). new: {k}: {self.properties[k]}"
                )
            else:
                print(f"{k} is not in properties")


class NotionPageContent:
    def __init__(self, body=None, contents=None, **kwargs):
        self.contents = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": body}}]
                },
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

    def update_contents_by_datetime(
        self, block_types, replace_str, date_format, start_date, increment=False
    ):
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
        start_dt = datetime.strptime(start_date, date_format)
        dt = start_dt
        for blk in self.contents:
            if blk["type"] not in SUPPORTED_BLOCK_TYPES:
                continue
            if blk["type"] in block_types:
                str_before = blk[blk["type"]]["rich_text"][0]["plain_text"]
                blk[blk["type"]]["rich_text"][0]["text"]["content"] = blk[blk["type"]][
                    "rich_text"
                ][0]["text"]["content"].replace(
                    replace_str,
                    dt.strftime(date_format),
                )
                blk[blk["type"]]["rich_text"][0]["plain_text"] = blk[blk["type"]][
                    "rich_text"
                ][0]["plain_text"].replace(
                    replace_str,
                    dt.strftime(date_format),
                )
                str_after = blk[blk["type"]]["rich_text"][0]["plain_text"]
                print(
                    f"updating contents type: {blk['type']}, {str_before=}, {str_after=}"
                )
                if increment is True:
                    dt += timedelta(days=1)


class NotionClient:
    def __init__(self):
        self.client = Client(auth=os.environ["NOTION_INTEGRATION_TOKEN"])

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
            res = self.client.pages.create(**pages_kwargs)
            print(f"page created successfully (id: {res['id']})")
            page_id = res["id"]
        else:
            page_id = pages[0]["id"]  # update the first matched page
            res = self.client.pages.update(page_id, **pages_kwargs)
            print(f"page updated successfully (id: {page_id})")

        # update contents
        self.update_contents(page_id=page_id, contents=content.contents)
        return {"id": res["id"]}

    def create_page_from_template(self, template_id, title, override=False, **kwargs):
        """Create a new page from the given template_id.
        if override is True and there's a page with the same title, update the existing page.
        You can pass values of properties via kwargs
        """

        # Prepare NotionPage and NotionPageContent from template
        tpl = self.get_page(page_id=template_id)
        if tpl["parent"]["type"] != "database_id":
            raise ValueError(
                "The given template_id {template_id} is not a database template."
            )
        database_id = tpl["parent"]["database_id"]
        pages_kwargs = NotionPage(  # only properties
            title=title,
            parent_type="database_id",
            properties=tpl["properties"],
            **kwargs,  # update properties
        ).pages_kwargs(parent_id=database_id)
        # To get contents of a page, Retrieve block children
        # https://developers.notion.com/reference/get-block-children
        child_blocks = self.get_child_blocks(block_id=template_id)
        content = NotionPageContent(contents=child_blocks["results"], **kwargs)

        # Create or update a page
        res = self.get_database(
            database_id=database_id,
            **{"filter": {"property": "title", "title": {"equals": title}}},
        )
        if len(res["results"]) == 0 or override is False:
            print(f"create a new page under database_id: {database_id}")
            res = self.client.pages.create(**pages_kwargs)  # create an empty page
            page_id = res["id"]
        else:
            page_id = res["results"][0]["id"]
            print(f"page with title '{title}' already exists (id: {page_id})")
            res = self.client.pages.update(
                page_id, **pages_kwargs
            )  # only update properties

        # update contents
        self.update_contents(page_id=page_id, contents=content.contents)

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
        """Query database
        1. get database with database_id
        2. search pages in the database
        Example:
            kwargs = {"filter": {"property": "title", "title": {"equals": "test"}}}
            get_database(database_id=database_id, **kwargs)

        """
        return self.client.databases.query(database_id=database_id, **kwargs)

    def get_child_blocks(self, block_id: str) -> dict:
        """Get children blocks.
        You can pass page_id to get the contents of a page.
        """
        return self.client.blocks.children.list(block_id)

    def update_contents(self, page_id: str, contents: dict):
        """Update a page with the given contents."""
        blk_children = self.client.blocks.children.list(page_id)
        print(f"{len(blk_children['results'])} blocks exist in page '{page_id}'")

        cur_size = len(blk_children["results"])
        # delete all existing blocks
        for i in range(cur_size):
            block_id = blk_children["results"][i]["id"]
            print(f"delete existing block {i} (block_id: {block_id})")
            self.client.blocks.delete(block_id=block_id)
        # append new blocks
        print("append new blocks")
        self.client.blocks.children.append(block_id=page_id, **{"children": contents})


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

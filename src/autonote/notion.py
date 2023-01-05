import argparse
import os

from notion_client import Client


class NotionMock:
    def create_page(self, parent_page_id, title, body):
        print(f"{parent_page_id=}, {title=}, {body=}")
        return {"id": "random_id"}


class NotionClient:
    def __init__(self):
        self.client = Client(auth=os.environ["NOTION_INTEGRATION_TOKEN"])

    def create_page(self, parent_page_id, title, body):
        """Create or update page.
        If there already exists pages with the given title,
        update the one with the latest last_edited_time.
        """
        kwargs = self.prepare_contents(
            parent_page_id=parent_page_id, title=title, body=body
        )
        page_id = self.get_page(query=title)
        if page_id is None:
            res = self.client.pages.create(**kwargs)
            print(f"page created successfully (id: {page_id}")
        else:
            print(f"page already exists (id: {page_id}")
            res = self.client.pages.update(page_id, **kwargs)
        return {"id": res["id"]}

    def prepare_contents(self, parent_page_id, title, body):
        return {
            "parent": {
                "type": "page_id",  # TODO: support database
                "page_id": parent_page_id,
            },
            "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": title},
                        }
                    ]
                }
            },
            "contents": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": body}}]
                    },
                },
            ],
        }

    def get_page(self, query):
        res = self.client.search(
            query=query,
            sort={
                "direction": "descending",
                "timestamp": "last_edited_time",
            },
        ).get("results")
        if len(res) == 0:
            return None
        if len(res) > 1:
            print(f"found {len(res)} pages matching with query '{query}'")
        return res[0]["id"]


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

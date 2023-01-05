import argparse
import os
import random

from atlassian import Confluence


class ConfluenceMock:
    def create_page(self, parent_page_id, title, body):
        print(f"{parent_page_id}, {title}, {body}")
        random_id = int("".join([str(random.randint(0, 10)) for _ in range(10)]))
        print(f"create page (dryrun) -> random id is generated {random_id}")
        return {"id": random_id}


class ConfluenceClient:
    def __init__(self):
        # https://xxx.atlassian.net
        confluence_url = os.getenv("CONFLUENCE_URL")
        self.confluence = Confluence(
            url=confluence_url,
            username=os.getenv("CONFLUENCE_USERNAME"),
            password=os.getenv("CONFLUENCE_PASSWORD"),
        )

    def create_page(self, parent_page_id, title, body):
        """Create or update page.
        If there already exists a page with the given title,
        update the existing page.
        """
        status = self.confluence.update_or_create(
            parent_page_id, title, body, editor="v2"
        )
        confluence_space_key = status["space"]["key"]
        print(f"create page -> key: {confluence_space_key} id: {status['id']}")
        return {"id": status["id"]}


def main():
    parser = argparse.ArgumentParser(description="Create Confluence page")
    parser.add_argument(
        "--confluence_parent_page_id",
        dest="confluence_parent_page_id",
        required=True,
        help="Confluence parent page id under which new Confluence pages will be created.",
    )
    parser.add_argument(
        "--dryrun",
        help="dryrun will not actually do the operation",
        action="store_true",
    )
    args = parser.parse_args()
    print(args)

    client = ConfluenceMock() if args.dryrun else ConfluenceClient()
    client.create_page(
        args.confluence_parent_page_id,
        title="title",
        body="body",
    )


if __name__ == "__main__":
    main()

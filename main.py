from confluence import ConfluenceClient, ConfluenceMock
from atlassian import Confluence
from html import generate, read
import argparse
import os

from dotenv import load_dotenv

load_dotenv()


confluence_url = os.getenv("CONFLUENCE_URL")  # https://xxx.atlassian.net
confluence = Confluence(
    url=confluence_url,
    username=os.getenv("CONFLUENCE_USERNAME"),
    password=os.getenv("CONFLUENCE_PASSWORD"),
)


def main():
    parser = argparse.ArgumentParser(description="generate lifelog")
    parser.add_argument(
        "--confluence_root_page_id",
        dest="confluence_root_page_id",
        required=True,
        help="Confluence root page id under which new Confluence pages will be created.",
    )
    parser.add_argument(
        "--dryrun",
        help="dryrun will not actually do the operation",
        action="store_true",
    )
    args = parser.parse_args()
    print(args)
    content = generate()

    client = ConfluenceMock() if args.dryrun else ConfluenceClient()
    client.create_page(
        args.confluence_root_page_id,
        title="monthly report",
        body=content,
    )


if __name__ == "__main__":
    main()

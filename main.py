import argparse
from datetime import date

from dotenv import load_dotenv

from autodoc.confluence import ConfluenceClient, ConfluenceMock
from autodoc.html import generate

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="autodoc")
    parser.add_argument(
        "--confluence_parent_page_id",
        dest="confluence_parent_page_id",
        required=True,
        help="Confluence parent page id under which new Confluence pages will be created.",
    )
    parser.add_argument(
        "--title",
        dest="title",
        required=False,
        default=f"default title {date.today().strftime('%Y-%m-%d')}",
        help="title of new page",
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
        args.confluence_parent_page_id,
        title=args.title,
        body=content,
    )


if __name__ == "__main__":
    main()

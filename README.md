# autodoc

## Description

![](docs/diagram.drawio.svg)

Automate creating daily, weekly, monthly, and quarterly manual repetitive documents:

1. Daily: daily journal, habit tracker
1. Weekly: weekly report
1. Monthly: monthly report
1. Quarterly: quarterly review

## Prerequisite

1. Confluence API Token

## Steps

1. Update env vars in `.env`

    ```
    CONFLUENCE_URL=https://xxx.atlassian.net
    CONFLUENCE_USERNAME=<yourname>@domain.com
    CONFLUENCE_PASSWORD=<TOKEN>
    ```

1. venv
    ```
    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    ```

1. Create Confluence Page
    ```
    python main.py --confluence_root_page_id <root_page_id>
    ```

    Generated Page:

    <table><tr><td>
    <img src="docs/confluence_page_0.png" width="200px" />
    </td></tr></table>



## References
1. [Pythonで久しぶりにHTMLを出力したくなったのでテンプレートについて調べる
](https://qiita.com/mima_ita/items/5405109b3b9e2db42332)

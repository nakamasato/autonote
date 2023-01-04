# autonote

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

1. Set environment variables:

    ```
    export CONFLUENCE_URL=https://xxx.atlassian.net
    export CONFLUENCE_USERNAME=<yourname>@domain.com
    export CONFLUENCE_PASSWORD=<TOKEN>
    ```

1. Install autonote
    ```
    pip install autonote
    ```

1. Run
    ```python
    from autonote.confluence import ConfluenceClient, ConfluenceMock
    from autonote.html import generate

    content = generate()
    ConfluenceClient().create_page(
        <confluence_parent_page_id>,
        title="title",
        body=content,
    )

    ```

    Generated Page:

    <table><tr><td>
    <img src="docs/confluence_page_0.png" width="200px" />
    </td></tr></table>

## Credits

`autonote` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`autonote` was created by Masato Naka. It is licensed under the terms of the MIT license.

## References
1. [How to package a Python](https://py-pkgs.org/03-how-to-package-a-python)
1. [py-pkgs-cookiecutter](https://github.com/py-pkgs/py-pkgs-cookiecutter)
1. [package](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

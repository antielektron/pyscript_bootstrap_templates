
import pathlib
from typing import List
import argparse


# create a new pyscript project

def create_project(root_folder: pathlib.Path,
                   title: str,
                   packages: List[str],
                   paths: List[str] = None,
                   pyscript_css_url: str = "https://pyscript.net/alpha/pyscript.css",
                   pyscript_js_url: str = "https://pyscript.net/alpha/pyscript.js"):

    pyenv = "- git+https://the-cake-is-a-lie.net/gogs/jonas/pyscript-bootstrap-templates.git"
    for package in packages:
        pyenv += f"\n            - {package}"

    if paths is not None:
        pyenv += "\n            - paths:"
        for path in paths:
            pyenv += f"\n                - {path}"

    pyenv += "\n"

    html = f"""
<!DOCTYPE html>
<html lang="en" style="width: 100%;height: 100%">
    <head id="head">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">


        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        <link rel="stylesheet" href="{pyscript_css_url}" />
        <script defer src="{pyscript_js_url}"></script>

        <title>{title}</title>
        
        <py-env>
            {pyenv}
        </py-env>
    </head>
    <body style="width: 100%; height: 100%">
        <div id="simple_app" style="height: 100%; min-height: 100%"></div>
        <py-script src="./main.py"></py-script>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

    </body>
</html>
    """

    py = f"""

    """

    if not root_folder.exists():
        root_folder.mkdir(parents=True)

    (root_folder / "index.html").write_text(html, encoding="utf-8")
    (root_folder / "main.py").write_text("", encoding="utf-8")


def main():

    argument_parser = argparse.ArgumentParser(
        description="create a new pyscript project")
    argument_parser.add_argument(
        "root_folder", type=pathlib.Path, help="the root folder of the new project")
    argument_parser.add_argument(
        "title", type=str, help="the title of the new project")
    argument_parser.add_argument(
        "packages", type=str, nargs="*", help="the packages to include in the new project")
    argument_parser.add_argument("--paths", type=str, nargs="+",
                                 help="additional local python files to include in the new project")
    argument_parser.add_argument("--pyscript_css_url", type=str,
                                 help="the url of the pyscript css file", default="https://pyscript.net/alpha/pyscript.css")
    argument_parser.add_argument("--pyscript_js_url", type=str,
                                 help="the url of the pyscript js file", default="https://pyscript.net/alpha/pyscript.js")
    arguments = argument_parser.parse_args()

    create_project(arguments.root_folder,
                   arguments.title,
                   arguments.packages,
                   arguments.paths,
                   arguments.pyscript_css_url,
                   arguments.pyscript_js_url)

if __name__ == "__main__":
    main()
    exit(0)
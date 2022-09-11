
from distutils.command.config import config
from multiprocessing.sharedctypes import Value
import pathlib
from typing import List
import argparse
from numpy import isin
import requests
import json
import shutil


def download_file(url: str, path: pathlib.Path):
    if pathlib.Path(url).exists():
        shutil.copy2(url, str(path))
    else:
        response = requests.get(url)
        path.write_bytes(response.content)


def generate_project_files(root_folder: pathlib.Path,
                   title: str,
                   packages: List[str],
                   paths: List[str] = None,
                   pyscript_css_url: str = "https://pyscript.net/alpha/pyscript.css",
                   pyscript_js_url: str = "https://pyscript.net/alpha/pyscript.min.js",
                   pyscript_py_url: str = "https://pyscript.net/alpha/pyscript.py",
                   bootstrap_css_url: str = "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
                   bootstrap_js_url: str = "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js",
                   pyscript_bootstrap_templates_wheel_url: str = "https://the-cake-is-a-lie.net/gogs/jonas/pyscript-bootstrap-templates/raw/branch/main/dist/pyscript_bootstrap_templates-0.1.0-py3-none-any.whl"):

    pyenv = f"- ./resources/{pyscript_bootstrap_templates_wheel_url.split('/')[-1]}"
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

        <link rel="stylesheet" href="./resources/pyscript.css" />
        <script defer src="./resources/pyscript.js"></script>

        <!-- Bootstrap CSS -->
        <link href="./resources/bootstrap.css" rel="stylesheet">

        <title>{title}</title>

        <py-env>
            {pyenv}
        </py-env>
    </head>
    <body style="width: 100%; height: 100%">
        <div id="pyscript_app" style="height: 100%; min-height: 100%"></div>
        <py-script src="./main.py"></py-script>

        <script src="./resources/bootstrap.js"></script>
    </body>
</html>
    """

    py = f"""
from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import HTML as HTML

app = bootstrap_templates.PyScriptBootstrapDashboard(
    parent_element="pyscript_app", brand_name="{title}")
div = bHTML.BootstrapContainer("This is a sidebar", parent=app.sidebar)
div.font_size = 4

btn = bHTML.ButtonPrimary("Click me", parent=app.sidebar)
btn.w = 100
btn.onclick = lambda _: bHTML.AlertSuccess(
    "You clicked me!", parent=app.main_area)
    """

    root_folder=pathlib.Path(root_folder)

    root_folder.mkdir(parents=True, exist_ok=True)
    (root_folder / "resources").mkdir(parents=True, exist_ok=True)

    # Download files:
    download_file(pyscript_css_url, root_folder / "resources" / "pyscript.css")
    download_file(pyscript_js_url, root_folder / "resources" / "pyscript.js")
    download_file(pyscript_py_url, root_folder / "resources" / "pyscript.py")
    download_file(bootstrap_css_url, root_folder /
                  "resources" / "bootstrap.css")
    download_file(bootstrap_js_url, root_folder / "resources" / "bootstrap.js")
    download_file(pyscript_bootstrap_templates_wheel_url,
                  root_folder / "resources" / pyscript_bootstrap_templates_wheel_url.split("/")[-1])

    index_html = (root_folder / "index.html")
    main_py = (root_folder / "main.py")

    index_html.write_text(html, encoding="utf-8")

    # only create if not existing:
    if not main_py.exists():
        main_py.write_text(py, encoding="utf-8")

def create_project(**kwargs):

    root_folder: pathlib.Path = kwargs['root_folder']
    
    if root_folder.exists():
        raise ValueError(f"cannot create project. Folder {str(root_folder)} already exists")
    
    root_folder.mkdir(parents=True, exist_ok=True)

    # create initial config.json

    kwargs['root_folder'] = str(root_folder)

    with open(root_folder / "config.json", 'w') as f:
        json.dump(kwargs, f, indent=4)
    
    generate_project_files(**kwargs)

def update_project(**kwargs):

    root_folder: pathlib.Path = kwargs['root_folder']
    if not root_folder.exists():
        raise ValueError(f"cannot update project in {str(root_folder)}. Path does not exist")
    
    # load config file
    config_json = root_folder / "config.json"
    if not config_json.exists():
        raise ValueError(f"cannot update project in {str(root_folder)}. Found no config.json inside give path")
    
    with open(config_json, "r") as f:
        config = json.load(f)
    
    # override config values that are not None or empty lists
    for arg, val in kwargs.items():
        if val is not None:
            if not isinstance(val, list) or len(val) > 0:
                config[arg] = val
    
    generate_project_files(**config)

    config['root_folder'] = str(root_folder)

    with open(root_folder / "config.json", 'w') as f:
        json.dump(config, f, indent=4)

def main():

    argument_parser = argparse.ArgumentParser(
        description="create a new pyscript project")

    argument_parser.add_argument("command", choices=["create","update"])
    
    argument_parser.add_argument(
        "root_folder", type=pathlib.Path, help="the root folder of the new project")
    argument_parser.add_argument(
        "title", type=str, help="the title of the new project")
    argument_parser.add_argument(
        "--packages", type=str, nargs="+", help="the packages to include in the new project")
    argument_parser.add_argument("--paths", type=str, nargs="+",
                                 help="additional local python files to include in the new project")
    argument_parser.add_argument("--pyscript_css_url", type=str,
                                 help="the url of the pyscript css file", default="https://pyscript.net/alpha/pyscript.css")
    argument_parser.add_argument("--pyscript_js_url", type=str,
                                 help="the url of the pyscript js file", default="https://pyscript.net/alpha/pyscript.min.js")
    argument_parser.add_argument("--pyscript_py_url", type=str,
                                    help="the url of the pyscript py file", default="https://pyscript.net/alpha/pyscript.py")
    argument_parser.add_argument("--bootstrap_css_url", type=str,
                                    help="the url of the bootstrap css file", default="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css")
    argument_parser.add_argument("--bootstrap_js_url", type=str,
                                    help="the url of the bootstrap js file", default="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js")
    argument_parser.add_argument("--pyscript_bootstrap_templates_wheel_url", type=str,
                                    help="the url of the pyscript bootstrap templates wheel file", default="https://the-cake-is-a-lie.net/gogs/jonas/pyscript-bootstrap-templates/raw/branch/main/dist/pyscript_bootstrap_templates-0.1.0-py3-none-any.whl")

    args = argument_parser.parse_args()

    config = {
        'root_folder': args.root_folder,
        'title': args.title,
        'packages': args.packages if args.packages is not None else [],
        'paths': args.paths if args.paths is not None else [],
        'pyscript_css_url': args.pyscript_css_url,
        'pyscript_js_url': args.pyscript_js_url,
        'pyscript_py_url': args.pyscript_py_url,
        'bootstrap_css_url': args.bootstrap_css_url,
        'bootstrap_js_url': args.bootstrap_js_url,
        'pyscript_bootstrap_templates_wheel_url': args.pyscript_bootstrap_templates_wheel_url
    }


    if args.command == "create":
        create_project(**config)
    elif args.command == "update":
        update_project(**config)
    else:
        # should never happen and be catched by argparse#
        raise ValueError("unknown command", args.command)


if __name__ == "__main__":
    main()
    exit(0)


from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


def get_version(rel_path):
    for line in (here / rel_path).read_text(encoding="utf-8").splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")



# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(

    name="pyscript-bootstrap-templates", 
    version=get_version("pyscript-bootstrap-templates/__init__.py"),
    description="templates and basic python/pyscript wrappers for bootstrap 5",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/pypa/sampleproject",

    author="Jonas Weinz",

    author_email="author@example.com",

    keywords="sample, setuptools, development",

    package_dir={"": "pyscript-bootstrap-templates"},
    packages=find_packages(where="pyscript-bootstrap-templates"),


    python_requires=">=3.7, <4",

    install_requires=[
        "pillow",
        "parse",
    ],

    entry_points={
        "console_scripts": [
            "create_pyscript_bootstrap_app=create:main",
        ],
    },

)


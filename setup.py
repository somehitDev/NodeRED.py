# -*- coding: utf-8 -*-
from setuptools import setup
from noderedpy import __version__, __author__, __email__


with open("requirements.txt", "r", encoding = "utf-8") as reqr:
    requires = [
        item.strip()
        for item in reqr.read().split("\n")
    ]

with open("README.md", "r", encoding = "utf-8") as rmr:
    readme = rmr.read()


setup(
    # publish informations
    name = "nodered.py",
    author = __author__,
    author_email = __email__,
    url = "https://github.com/oyajiDev/NodeRED.py",
    version = __version__,
    python_requires = ">=3.9",
    install_requires = requires,
    setup_requires = requires,
    license = "MIT license",
    description = "make python function to Node-RED node",
    long_description = readme,
    long_description_content_type = "text/markdown",
    # package informations
    packages = [
        "noderedpy", "noderedpy/assets", "noderedpy/templates", "noderedpy/node-red-starter"
    ],
    package_data = {
        "": [
            "*.png", "*.html", "*.js", "*.json"
        ]
    },
    include_package_data = True,
    zip_safe = True
)

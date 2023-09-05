# -*- coding: utf-8 -*-
import json
from typing import List


def package_json(name:str, version:str, description:str, author:str, keywords:List[str]) -> str:
    if not "node-red" in keywords:
        keywords.append("node-red")

    return json.dumps({
        "name": name,
        "version": version,
        "description": description,
        "author": author,
        "keywords": keywords,
        "node-red": {
            "nodes": {
                name: f"lib/{name}.js"
            }
        }
    }, indent = 4)

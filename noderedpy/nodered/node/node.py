# -*- coding: utf-8 -*-
import os, gc, traceback
from types import MethodType
from typing import List
from ..red.editor.widget import Widget
from ..red.editor.editor import Editor
from .communicator import NodeCommunicator
from ...templates.package import package_json
from ...templates.html import node_html
from ...templates.javascript import node_js
from .. import __path__



class Node:
    def __init__(self, name:str, category:str, version:str, description:str, author:str, keywords:List[str], icon:str, color:str, widgets:List[Widget], node_func:MethodType):
        # name of node cannot contain spaces
        if " " in name.strip():
            raise NameError("Node name cannot contain spaces!")
        
        # category of node cannot contain - or ,
        if "-" in category.strip() or "," in category.strip():
            raise NameError("Category cannot contain '-' or ','!")
        
        # remove default keyword in extra keywords
        self.keywords = [
            keyword
            for keyword in keywords
            if not keyword in ( "node-red", )
        ]

        self.name, self.category, self.version, self.description, self.author, self.icon, self.color, self.editor =\
            name, category, version, description, author, icon, color, Editor(widgets)

        self.__node_func = node_func

    def create(self, node_red_user_dir:str, node_red_user_cache_dir:str):
        self.__communicator = NodeCommunicator(os.path.join(node_red_user_cache_dir, "node_message.json"), self.name)
        node_dir = os.path.join(node_red_user_dir, "node_modules", self.name if self.name.startswith("nodered-py-") else f"nodered-py-{self.name}")
        os.makedirs(os.path.join(node_dir, "lib"))

        # render editor
        rendered_editor = self.editor.render()
        self.__props_map = rendered_editor.props_map

        # write package.json
        with open(os.path.join(node_dir, "package.json"), "w", encoding = "utf-8") as pjw:
            pjw.write(package_json(self.name, self.version, self.description, self.author, self.keywords))

        # write html
        with open(os.path.join(node_dir, "lib", f"{self.name}.html"), "w", encoding = "utf-8") as nhw:
            nhw.write(node_html(
                self.name, self.icon, self.category, self.color,
                rendered_editor.html, rendered_editor.props,
                rendered_editor.prepare,
                rendered_editor.cancel, rendered_editor.save
            ))

        # write javascript
        with open(os.path.join(node_dir, "lib", f"{self.name}.js"), "w", encoding = "utf-8") as njw:
            njw.write(node_js(self.name, [ name for name in rendered_editor.props.keys() if not name == "name" ], node_red_user_cache_dir))

    def run(self, raw_props:dict, msg:dict) -> dict:
        gc.enable()

        print(f"\n{self.name} started\n===================================")
        try:
            props = {}
            for name, map_info in self.__props_map.items():
                if isinstance(map_info, list):
                    props[name] = [
                        raw_props[var_name]
                        for var_name in map_info
                    ]
                elif isinstance(map_info, dict):
                    props[name] = {
                        key: raw_props[var_name]
                        for key, var_name in map_info.items()
                    }
                else:
                    props[name] = raw_props[map_info]

            resp = self.__node_func(self.__communicator, props, msg)
            del props
            print("============================= ended\n")

            resp.update({ "state": "success", "name": self.name })
            gc.collect()

            return resp
        except:
            return { "state": "fail", "name": self.name, "message": traceback.format_exc() }

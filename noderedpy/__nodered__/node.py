# -*- coding: utf-8 -*-
import os, gc, json, traceback
from types import MethodType
from typing import List, Literal
from ..templates import package_json, node_html, node_js
from ..__property__ import Property
from .. import __path__



class Node:
    def __init__(self, name:str, category:str, version:str, description:str, author:str, keywords:List[str], icon:str, properties:List[Property], node_func:MethodType):
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

        self.name, self.category, self.version, self.description, self.author, self.icon, self.properties =\
            name, category, version, description, author, icon, properties

        self.__node_func = node_func

    def create(self, node_red_user_dir:str, node_red_user_cache_dir:str):
        self.__communicator = NodeCommunicator(os.path.join(node_red_user_cache_dir, "node_message.json"), self.name)
        node_dir = os.path.join(node_red_user_dir, "node_modules", self.name if self.name.startswith("nodered-py-") else f"nodered-py-{self.name}")
        os.makedirs(os.path.join(node_dir, "lib"))

        with open(os.path.join(node_dir, "package.json"), "w", encoding = "utf-8") as pjw:
            pjw.write(package_json(self))

        with open(os.path.join(node_dir, "lib", f"{self.name}.html"), "w", encoding = "utf-8") as nhw:
            nhw.write(node_html(self))

        with open(os.path.join(node_dir, "lib", f"{self.name}.js"), "w", encoding = "utf-8") as njw:
            njw.write(node_js(self, node_red_user_cache_dir))

    def run(self, props:dict, msg:dict) -> dict:
        gc.enable()

        print(f"\n{self.name} started\n===================================")
        try:
            resp = self.__node_func(self.__communicator, props, msg)
            print("============================= ended\n")

            resp.update({ "state": "success", "name": self.name })
            gc.collect()

            return resp
        except:
            return { "state": "fail", "name": self.name, "message": traceback.format_exc() }


class NodeCommunicator:
    def __init__(self, message_file:str, node_name:str):
        self.__message_file, self.__node_name = message_file, node_name

    def log(self, *args):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "log": args
            }, mfw, indent = 4)

    def warn(self, *args):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "warn": args
            }, mfw, indent = 4)

    def error(self, *args):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "error": args
            }, mfw, indent = 4)

    def status(self, fill:Literal["red", "green", "yellow", "blue", "grey"], shape:Literal["ring", "dot"], text:str):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "status": { "fill": fill, "shape": shape, "text": text }
            }, mfw, indent = 4)

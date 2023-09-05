# -*- coding: utf-8 -*-
import json
from typing import Literal


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

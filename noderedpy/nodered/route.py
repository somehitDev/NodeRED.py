# -*- coding: utf-8 -*-
import os, gc, traceback
from types import MethodType


class Route:
    def __init__(self, url:str, method:str, target:MethodType):
        # check url is valid
        if not url.startswith("/"):
            raise ValueError("url must starts with `/`!")

        self.url, self.method = url, method
        self.__target = target

    def run(self, route_data:dict) -> dict:
        gc.enable()

        print(f"\n{self.method} | {self.url} entered\n=============================================")
        try:
            data = self.__target(route_data)

            print("======================================= ended\n")
            gc.collect()

            return { "state": "success", "data": data }
        except:
            return { "state": "fail", "message": traceback.format_exc() }
        
    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "method": self.method
        }

class StaticRoute(Route):
    def __init__(self, url:str, path:os.PathLike):
        super().__init__(url, "static", None)
        self.path = path

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "method": "static",
            "path": self.path
        }

# -*- coding: utf-8 -*-
from typing import List, Literal
from types import MethodType
from .__nodered__.red import RED
from .__nodered__.node import Node
from .__property__ import Property
from .__nodered__.route import Route


def register(name:str, category:str = "nodered_py", version:str = "1.0.0", description:str = "", author:str = "nodered.py", keywords:List[str] = [], icon:str = "function.png", properties:List[Property] = []) -> MethodType:
    """
    Decorator to register Node function

    Parameters
    ----------
    name: str, required
        name of Node to register
    category: str, default nodered_py
        category of Node
    version: str, default 1.0.0
        version of Node
    description: str, default ""
        description of Node
    author: str, default nodered.py
        author of Node
    keywords: List[str], default []
        extra keywords of Node
    icon: str, default function.png
        icon of Node(html)
    properties: List[noderedpy._property.Property]
        propertis of Node
    """
    def decorator(node_func:MethodType):
        RED.registered_nodes.append(
            Node(
                name, category,
                version, description, author, keywords,
                icon, properties, node_func
            )
        )

        return node_func
    
    return decorator

def route(url:str, method:Literal["get", "post"]) -> MethodType:
    """
    Decorator to register route to Node-RED

    Parameters
    ----------
    url: str, required
        url of route point
    method: str, required
        method of route point
        options: get, post
    """
    def decorator(route_func:MethodType):
        RED.registered_routes.append(
            Route(url, method, route_func)
        )

        return route_func
    
    return decorator

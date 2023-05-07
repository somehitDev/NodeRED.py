# -*- coding: utf-8 -*-
from typing import List
from types import MethodType
from ._nodered import RED, Node
from ._property import Property
from ._server import Server


def register(name:str, category:str = "nodered_py", properties:List[Property] = []) -> MethodType:
    """
    Decorator to register Node function

    Parameters
    ----------
    name: str, required
        name of Node to register
    category: str, default nodered_py
        category of Node
    properties: List[noderedpy._property.Property]
        propertis of Node
    """
    def decorator(node_func:MethodType):
        node = Node(name if name.startswith("nodered-py") else f"nodered-py-{name}", category, properties, node_func)
        RED.registered_nodes.append(node)

        return node_func
    
    return decorator

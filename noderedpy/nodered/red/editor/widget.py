# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Dict, Union, List
from htmlgenerator import HTMLElement
from abc import ABCMeta, abstractmethod


@dataclass
class RenderedWidget:
    """
    Class for return of Widget.render()

    Attributes
    ----------
    props: dict, default {}
        information of properties
    props_map: Dict[str, Union[str, List[str], Dict[str, str]]], default {}
        information of mapping properties for node_function
    elements: List[HTMLElement], default []
        elements of Node-RED editor dialog
    prepare: str, default ""
        oneditprepare function script of Widget in Node
    cancel: str, default ""
        oneditcancel function script of Widget in Node
    save: str, default ""
        oneditsave function script of Widget in Node
    """
    props:dict = field(default_factory = dict)
    props_map:Dict[str, Union[str, List[str], Dict[str, str]]] = field(default_factory = dict)
    elements:List[HTMLElement] = field(default_factory = list)
    prepare:str = ""
    cancel:str = ""
    save:str = ""

class Widget(metaclass = ABCMeta):
    @abstractmethod
    def render(self) -> RenderedWidget:
        pass

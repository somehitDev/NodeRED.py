# -*- coding: utf-8 -*-
from typing import Dict, Union, List, Any
from dataclasses import dataclass, field
from htmlgenerator import HTMLElement
from abc import abstractmethod
from ...red.editor.widget import Widget, RenderedWidget


@dataclass
class RenderedProperty(RenderedWidget):
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

class Property(Widget):
    def __init__(self, name:str, default:Any = None, required:bool = False, tooltip:str = "", display_name:str = None, display_icon:str = None):
        super().__init__()

        self.name, self.default, self.required, self.tooltip, self.display_icon =\
            name, default, required, tooltip, display_icon
        self.display_name = " ".join([ item.strip().capitalize() for item in name.split("_") ]) if display_name is None else display_name
    
    @property
    def var_name(self) -> str:
        name_for_id = self.name.lower()\
            .replace(
                " ", "_"
            ).replace(
                ".", "_"
            ).replace(
                ":", "_"
            )

        return f"np-var_{name_for_id}"
    
    @abstractmethod
    def render(self) -> RenderedProperty:
        pass

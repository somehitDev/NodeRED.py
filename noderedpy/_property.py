# -*- coding: utf-8 -*-
import json
from typing import Any, Union, List



class Property:
    def __init__(self, name:str, default:Any = None, required:bool = False, display_icon:str = None):
        self.name, self.default, self.required, self.display_icon =\
            name, default, required, display_icon
        
    @property
    def display_name(self) -> str:
        return " ".join([
            item.capitalize()
            for item in self.name.split("_")
        ])

class CodeProperty(Property):
    def __init__(self, name:str, default:str = "", language:str = None, height:int = 250, required:bool = False, display_icon:str = None):
        if not isinstance(default, str):
            raise TypeError("CodeProperty can accept types: [ 'dict', 'json string' ]")
        
        super().__init__(name, default, required, display_icon if display_icon else "fa fa-code")
        self.language, self.height =\
            language, height

class InputProperty(Property):
    def __init__(self, name:str, default:Union[int, float, str] = None, required:bool = False, display_icon:str = None):
        if not isinstance(default, (int, float, str)):
            raise TypeError("InputProperty can accept types: [ 'int', 'float', 'str' ]")
        
        if default is None:
            if isinstance(default, int):
                default = 0
            elif isinstance(default, float):
                default = 0.0
            else:
                default = ""

        super().__init__(name, default, required, display_icon)

        if display_icon is None:
            if isinstance(default, (int, float)):
                self.display_icon = "fa fa-sort-numeric-asc"
            else:
                self.display_icon = "fa fa-font"
        else:
            self.display_icon = display_icon

class ListProperty(Property):
    def __init__(self, name:str, default:list = [], height:int = 250, required:bool = False, display_icon:str = None):
        if not isinstance(default, list):
            raise TypeError("ListProperty can accept type: 'list'")

        super().__init__(name, default, required, display_icon if display_icon else "fa fa-list-ul")
        self.height = height

class DictProperty(CodeProperty):
    def __init__(self, name:str, default:Union[dict, str] = {}, height:int = 250, required:bool = False, display_icon:str = None):
        if not isinstance(default, ( dict, str )):
            raise TypeError("DictProperty can accept types: [ 'dict', 'json string' ]")
        
        if isinstance(default, str):
            if not default.strip().startswith("{") or not default.strip().endswith("}"):
                raise ValueError("DictProperty value must be 'dict' or 'json string'!")

            try:
                json.loads(default)
            except:
                raise ValueError("DictProperty value must be 'dict' or 'json string'!")

        if isinstance(default, dict):
            default = json.dumps(default, indent = 4)

        super().__init__(name, default, "json", height, required, display_icon if display_icon else "fa fa-code")

class SpinnerProperty(Property):
    def __init__(self, name:str, default:float = 0, step:float = None, min:float = None, max:float = None, required:bool = False, display_icon:str = None):
        if not isinstance(default, (int, float)):
            raise TypeError("SpinnerProperty can accept types: [ 'int', 'float' ]")

        super().__init__(name, default, required, display_icon if display_icon else "fa fa-random")
        self.step, self.min, self.max =\
            step, min, max

class ComboBoxProperty(Property):
    def __init__(self, name:str, items:List[Any], default:str = None, required:bool = False, display_icon:str = None):
        if not isinstance(items, list):
            raise TypeError("items of ComboBoxProperty must be type: 'list'")
        
        super().__init__(name, default, required, display_icon if display_icon else "fa fa-filter")
        self.items = items

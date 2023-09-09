# -*- coding: utf-8 -*-
import json
from typing import Union
from .code import Code


class Dict(Code):
    def __init__(self, name:str, default:Union[dict, str] = {}, height:int = 250, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to handle dict

        name: str, required
            name of Dictroperty
        default: Union[dict, str], default {}
            default value of DictProperty
        height: int, default 250
            height to display in Node-RED edit dialog
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
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

        super().__init__(name, default, "json", height, required, display_name, display_icon if display_icon else "fa fa-file-code-o")

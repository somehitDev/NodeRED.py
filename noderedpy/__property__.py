# -*- coding: utf-8 -*-
import json
from typing import Any, Union, List



class Property:
    def __init__(self, name:str, default:Any = None, required:bool = False, display_name:str = None, display_icon:str = None):
        self.name, self.default, self.required, self.display_icon =\
            name, default, required, display_icon
        self.display_name = " ".join([ item.strip().capitalize() for item in name.split("_") ]) if display_name is None else display_name
    
    @property
    def var_name(self) -> str:
        return f"np-var_{self.name}"

class CodeProperty(Property):
    def __init__(self, name:str, default:str = "", language:str = None, height:int = 250, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to edit code

        name: str, required
            name of CodeProperty
        default: str, default ""
            default value of CodeProperty
        language: str, default None
            language mode("ace/mode/") of Node-RED Editor
        height: int, default 250
            height to display in Node-RED edit dialog
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if not isinstance(default, str):
            raise TypeError("CodeProperty can accept types: [ 'dict', 'json string' ]")
        
        super().__init__(name, default, required, display_name, display_icon if display_icon else "fa fa-code")
        self.language, self.height =\
            language, height

class InputProperty(Property):
    def __init__(self, name:str, default:Union[int, float, str] = None, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to change value

        name: str, required
            name of InputProperty
        default: Union[int, float, str], default ""
            default value of InputProperty
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if default is None:
            if isinstance(default, int):
                default = 0
            elif isinstance(default, float):
                default = 0.0
            else:
                default = ""
        elif not isinstance(default, (int, float, str)):
            raise TypeError("InputProperty can accept types: [ 'int', 'float', 'str' ]")

        super().__init__(name, default, required, display_name, display_icon)

        if display_icon is None:
            if isinstance(default, (int, float)):
                self.display_icon = "fa fa-sort-numeric-asc"
            else:
                self.display_icon = "fa fa-font"
        else:
            self.display_icon = display_icon

class ListProperty(Property):
    def __init__(self, name:str, default:list = [], height:int = 250, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to handle list

        name: str, required
            name of ListProperty
        default: list, default []
            default value of ListProperty
        height: int, default 250
            height to display in Node-RED edit dialog
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if not isinstance(default, list):
            raise TypeError("ListProperty can accept type: 'list'")

        super().__init__(name, default, required, display_name, display_icon if display_icon else "fa fa-list-ul")
        self.height = height

class DictProperty(CodeProperty):
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

class SpinnerProperty(Property):
    def __init__(self, name:str, default:float = 0, step:float = None, min:float = None, max:float = None, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to handle float with spinner

        name: str, required
            name of SpinnerProperty
        default: float, default 0
            default value of SpinnerProperty
        step: float, default None
            step for spinner
        min: float, default None
            min value for spinner
        max: float, default None
            max value for spinner
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if not isinstance(default, (int, float)):
            raise TypeError("SpinnerProperty can accept types: [ 'int', 'float' ]")

        super().__init__(name, default, required, display_name, display_icon if display_icon else "fa fa-random")
        self.step, self.min, self.max =\
            step, min, max

class CheckBoxProperty(Property):
    def __init__(self, name:str, default:bool = False, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to handle checked state

        name: str, required
            name of CheckBoxProperty
        default: bool, default False
            default value of CheckBoxProperty
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        super().__init__(name, default, required, display_name, display_icon if display_icon else "fa fa-check")

class ComboBoxProperty(Property):
    def __init__(self, name:str, items:List[Any], default:Any = None, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to select value from lists

        name: str, required
            name of ComboBoxProperty
        items: List[Any], required
            items of ComboBoxProperty
        default: Any, default None
            default value of ComboBoxProperty
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if not isinstance(items, list):
            raise TypeError("items of ComboBoxProperty must be type: 'list'")
        
        if default is None:
            if len(items) > 0:
                default = items[0]
            else:
                default = ""
        
        super().__init__(name, default, required, display_name, display_icon if display_icon else "fa fa-filter")
        self.items = items

# class FileProperty(Property):
#     def __init__(self, name:str, default:str = None, required:bool = False, display_icon:str = None):
#         super().__init__(name, default if default else "", required, display_icon if display_icon else "fa fa-file-text-o")

# class TableProperty(Property):
#     def __init__(self, name:str, default:pd.DataFrame = None, required:bool = False, display_icon:str = None):
#         super().__init__(name, default if default else pd.DataFrame(), required, display_icon if display_icon else "fa fa-table")

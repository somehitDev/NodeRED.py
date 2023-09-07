# -*- coding: utf-8 -*-
from typing import Any


class Property:
    def __init__(self, name:str, default:Any = None, required:bool = False, display_name:str = None, display_icon:str = None):
        self.name, self.default, self.required, self.display_icon =\
            name, default, required, display_icon
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

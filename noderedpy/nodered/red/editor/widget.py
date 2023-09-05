# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict, Union, List
from abc import ABCMeta, abstractmethod


@dataclass
class RenderedWidget:
    props:dict
    props_map:Dict[str, Union[str, List[str], Dict[str, str]]]
    html:str
    prepare:str
    cancel:str
    save:str

class Widget(metaclass = ABCMeta):
    @abstractmethod
    def render(self) -> RenderedWidget:
        pass

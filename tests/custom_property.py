# -*- coding: utf-8 -*-
import htmlgenerator as hg
from noderedpy.nodered.node.properties.property import Property, RenderedProperty


class MyProperty(Property):
    def __init__(self):
        super().__init__("my_property", required = True)

    def render(self) -> RenderedProperty:
        return RenderedProperty(
            props = {}, props_map = {},
            elements = [ hg.DIV() ],
            prepare = "", cancel = "", save = ""
        )

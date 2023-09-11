# -*- coding: utf-8 -*-
import htmlgenerator as hg
from noderedpy.nodered.red.editor.widget import Widget, RenderedWidget


class MyWidget(Widget):
    def __init__(self):
        super().__init__()

    def render(self) -> RenderedWidget:
        return RenderedWidget(
            props = {}, props_map = {},
            elements = [ hg.DIV() ],
            prepare = "", cancel = "", save = ""
        )

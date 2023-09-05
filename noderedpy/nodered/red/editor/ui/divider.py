# -*- coding: utf-8 -*-
from ..widget import Widget, RenderedWidget


class Divider(Widget):
    def render(self) -> RenderedWidget:
        return RenderedWidget(
            props = {}, props_map = {},
            html = "<hr>",
            prepare = "", cancel = "", save = ""
        )

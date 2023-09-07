# -*- coding: utf-8 -*-
import htmlgenerator as hg
from ..widget import Widget, RenderedWidget


class Divider(Widget):
    def render(self) -> RenderedWidget:
        return RenderedWidget(
            elements = [ hg.HR() ]
        )

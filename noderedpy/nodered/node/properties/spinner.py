# -*- coding: utf-8 -*-
import htmlgenerator as hg
from .property import Property
from ...red.editor.widget import Widget, RenderedWidget


class SpinnerProperty(Property, Widget):
    def __init__(self, name:str, default:float = 0, step:float = None, min:float = None, max:float = None, required:bool = False, display_name:str = None, display_icon:str = None, one_line:bool = False):
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

        Property.__init__(self, name, default, required, display_name, display_icon if display_icon else "fa fa-random")
        Widget.__init__(self)
        self.step, self.min, self.max =\
            step, min, max
        self.one_line = one_line

    def render(self) -> RenderedWidget:
        rendered = RenderedWidget(
            props = { self.var_name: { "value": self.default, "required": self.required } },
            props_map = { self.name: self.name },
            html = "",
            prepare = "", cancel = "", save = ""
        )

        if self.one_line:
            rendered.html = hg.render(
                hg.DIV(
                    hg.LABEL(
                        hg.I(_class = self.display_icon, style = "margin-right:5px;"),
                        hg.SPAN(self.display_name),
                        style = "display:flex;align-items:center;margin-right:10px;"
                    ),
                    hg.INPUT(
                        id = f"node-input-{self.var_name}",
                        type = "text",
                        style = "width:100%;"
                    ),
                    _class = "form-row",
                    style = "display:flex;flex-flow:row;",
                    **{ "data-flex": "true" }
                ), {}
            )
        else:
            rendered.html = hg.render(
                hg.DIV(
                    hg.LABEL(
                        hg.I(_class = self.display_icon), " ",
                        hg.SPAN(self.display_name)
                    ),
                    _class = "form-row",
                    style = "margin-bottom: 0px;"
                ), {}
            ) + hg.render(
                hg.DIV(
                    hg.INPUT(
                        id = f"node-input-{self.var_name}",
                        type = "text",
                        style = "width: 100%;"
                    ),
                    _class = "form-row"
                ), {}
            )

        spinner_configs = []
        if self.min:
            spinner_configs.append(f"min: {self.min}")
        if self.max:
            spinner_configs.append(f"max: {self.max}")
        if self.step:
            spinner_configs.append(f"step: {self.step}")

        rendered.prepare = """
            $('#node-input-""" + self.var_name + """').spinner({
                """ + ",\n                ".join(spinner_configs) + """
            });
"""

        return rendered

# -*- coding: utf-8 -*-
import htmlgenerator as hg
from .property import Property, RenderedProperty


class CheckBox(Property):
    def __init__(self, name:str, default:bool = False, required:bool = False, tooltip:str = "", display_name:str = None, display_icon:str = None):
        """
        Property to handle checked state

        name: str, required
            name of CheckBoxProperty
        default: bool, default False
            default value of CheckBoxProperty
        required: bool, default False
            set required or not
        tooltip: str, default ""
            tooltip of CheckBoxProperty
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        super().__init__(name, default, required, tooltip, display_name, display_icon if display_icon else "fa fa-check")

    def render(self) -> RenderedProperty:
        rendered = RenderedProperty(
            props = { self.var_name: { "value": self.default, "required": self.required } },
            props_map = { self.name: self.name }
        )

        eid = f"node-input-{self.var_name}"
        rendered.elements.append(
            hg.DIV(
                hg.LABEL(
                    hg.I(_class = self.display_icon), " ",
                    hg.SPAN(self.display_name),
                    **{ "for": eid, "title": self.tooltip }
                ),
                hg.INPUT(
                    id = eid,
                    type = "checkbox",
                    style = "margin-left:10px;width:15px;height:15px;margin-bottom:5px;"
                ),
                _class = "form-row"
            )
        )

        return rendered

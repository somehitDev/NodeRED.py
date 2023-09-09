# -*- coding: utf-8 -*-
import htmlgenerator as hg, json
from typing import Dict, Any, List
try:
    from typing import Literal
except:
    from typing_extensions import Literal

from .property import Property
from ...red.editor.widget import Widget, RenderedWidget


class TypedInput(Property, Widget):
    def __init__(self, name:str, default:Dict[Literal["type", "value"], Any] = {}, types:List[str] = [], required:bool = False, display_name:str = None, display_icon:str = None, one_line:bool = False):
        """
        Property to change value

        name: str, required
            name of TypedInputProperty
        default: Dict[Literal["type", "value"], Any], default {}
            default value of TypedInputProperty
        type: List[str], default []
            types of TypedInputProperty
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        Property.__init__(self, name, default, required, display_name, display_icon if display_icon else "fa fa-sort-alpha-asc")
        Widget.__init__(self)

        self.default = {
            "type": self.default.pop("type", types[0] if len(types) > 0 else ""),
            "value": self.default.pop("value", None)
        }
        self.types = types
        self.one_line = one_line

    def render(self) -> RenderedWidget:
        rendered = RenderedWidget(
            props = {
                f"{self.var_name}-typed-input-type": { "value": self.default["type"] },
                f"{self.var_name}-typed-input-value": { "value": self.default["value"], "required": self.required }
            },
            props_map = {
                self.name: {
                    "type": f"{self.name}-typed-input-type",
                    "value": f"{self.name}-typed-input-value"
                }
            }
        )

        eid = f"node-input-{self.var_name}-typed-input"
        if self.one_line:
            rendered.elements.append(
                hg.DIV(
                    hg.LABEL(
                        hg.I(_class = self.display_icon, style = "margin-right:5px;"),
                        hg.SPAN(self.display_name),
                        style = "display:flex;align-items:center;",
                        **{ "for": eid }
                    ),
                    hg.INPUT(
                        id = eid,
                        type = "text",
                        style = "margin-left:10px;flex:1;"
                    ),
                    hg.INPUT(
                        id = f"{eid}-type",
                        type = "text",
                        style = "display:none;"
                    ),
                    hg.INPUT(
                        id = f"{eid}-value",
                        type = "text",
                        style = "display:none;"
                    ),
                    _class = "form-row",
                    style = "display:flex;flex-flow:row;"
                )
            )
        else:
            rendered.elements.extend([
                hg.DIV(
                    hg.LABEL(
                        hg.I(_class = self.display_icon), " ",
                        hg.SPAN(self.display_name)
                    ),
                    _class = "form-row",
                    style = "margin-bottom: 0px;",
                    **{ "for": eid }
                ),
                hg.DIV(
                    hg.INPUT(
                        id = eid,
                        type = "text",
                        style = "width:100%;"
                    ),
                    hg.INPUT(
                        id = f"{eid}-type",
                        type = "text",
                        style = "display:none;"
                    ),
                    hg.INPUT(
                        id = f"{eid}-value",
                        type = "text",
                        style = "display:none;"
                    ),
                    _class = "form-row"
                )
            ])

        type_maps = [
            { "value": type, "label": f"{type}:", "hasValue": True }
            for type in self.types
        ]
        rendered.prepare = """
            $('#node-input-""" + self.var_name + """-typed-input').typedInput({
                default: '""" + self.default["type"] + """',
                types: """ + json.dumps(type_maps) + """,
                typeField: $('#node-input-""" + self.var_name + """-type')
            })

            $('#node-input-""" + self.var_name + """-typed-input').typedInput('type', node['""" + self.var_name + """-typed-input-type']);
            $('#node-input-""" + self.var_name + """-typed-input').typedInput('value', node['""" + self.var_name + """-typed-input-value']);
"""

        return rendered

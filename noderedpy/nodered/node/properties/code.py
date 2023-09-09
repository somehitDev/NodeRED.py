# -*- coding: utf-8 -*-
import htmlgenerator as hg
from .property import Property
from ...red.editor.widget import Widget, RenderedWidget


class Code(Property, Widget):
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
        
        Property.__init__(self, name, default, required, display_name, display_icon if display_icon else "fa fa-code")
        Widget.__init__(self)
        self.language, self.height =\
            language, height

    def render(self) -> RenderedWidget:
        rendered = RenderedWidget(
            props = { self.var_name: { "value": self.default, "required": self.required } },
            props_map = { self.name: self.name }
        )

        rendered.elements.extend([
            hg.DIV(
                hg.LABEL(
                    hg.I(_class = self.display_icon), " ",
                    hg.SPAN(self.display_name)
                ),
                _class = "form-row",
                style = "margin-bottom: 0px;",
                **{ "for": f"node-input-{self.var_name}" }
            ),
            hg.DIV(
                hg.DIV(
                    id = f"node-input-{self.var_name}",
                    _class = "node-text-editor",
                    style = f"height:{self.height}px"
                ),
                _class = "form-row node-text-editor-row"
            )
        ])

        code_configs = [
            f'id: "node-input-{self.var_name}"',
            f'value: node["{self.var_name}"]',
            "focus: true"
        ]
        if self.language:
            code_configs.append(
                f'mode: "ace/mode/{self.language}"'
            )
        
        rendered.prepare = """
            node['""" + self.var_name + """-editor'] = RED.editor.createEditor({
                """ + ",\n                ".join(code_configs) + """
            });
"""
        rendered.cancel = f"""
            node["{self.var_name}-editor"].destroy();
            delete node["{self.var_name}-editor"];"""
        rendered.save = f"""
            $("#node-input-{self.var_name}").val(node["{self.var_name}-editor"].getValue().trim());
            node["{self.var_name}-editor"].destroy();
            delete node["{self.var_name}-editor"];"""

        return rendered

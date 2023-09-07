# -*- coding: utf-8 -*-
import htmlgenerator as hg
from .property import Property
from ...red.editor.widget import Widget, RenderedWidget


class ListProperty(Property, Widget):
    def __init__(self, name:str, default:list = [], height:int = 250, required:bool = False, display_name:str = None, display_icon:str = None):
        """
        Property to handle list

        name: str, required
            name of ListProperty
        default: list, default []
            default value of ListProperty
        height: int, default 250
            height to display in Node-RED edit dialog
        required: bool, default False
            set required or not
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if not isinstance(default, list):
            raise TypeError("ListProperty can accept type: 'list'")

        Property.__init__(self, name, default, required, display_name, display_icon if display_icon else "fa fa-list-ul")
        Widget.__init__(self)
        self.height = height

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
                style = "margin-bottom: 0px;"
            ),
            hg.DIV(
                hg.OL(
                    id = f"node-input-{self.var_name}-container",
                    style = f"height:{self.height}px;"
                ),
                _class = f"form-row node-input-{self.var_name}-container-row"
            )
        ])
        rendered.prepare = """
            $('#node-input-""" + self.var_name + """-container').editableList({
                addItem: (container, idx, opt) => {
                    opt.idx = idx;
                    opt.value = opt.value ?? "";
                    
                    container.css({ overflow: "hidden", display: "flex", "align-items": "center" });
                    $("<input>", { class: "input-list-item", type: "text", style:"flex:1;" }).val(opt.value).appendTo(container);
                },
                removable: true
            })

            for (var item of node['""" + self.var_name + """']) {
                $('#node-input-""" + self.var_name + """-container').editableList("addItem", { value: item });
            }
"""
        rendered.save = """
            node['""" + self.var_name + """'] = [];
            $('#node-input-""" + self.var_name + """-container').editableList("items").each((_, item) => {
                node['""" + self.var_name + """'].push(item.find("input.input-list-item").val());
            });
"""

        return rendered

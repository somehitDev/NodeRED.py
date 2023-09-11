# -*- coding: utf-8 -*-
import htmlgenerator as hg
from .property import Property, RenderedProperty


class List(Property):
    def __init__(self, name:str, default:list = [], height:int = 250, required:bool = False, tooltip:str = "", display_name:str = None, display_icon:str = None):
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
        tooltip: str, default ""
            tooltip for ListProperty
        display_name: str, default None
            name to display in Node-RED edit dialog
        display_icon: str, default None
            icon to display in Node-RED edit dialog (for available icons, see https://fontawesome.com/v4/icons/)
        """
        if not isinstance(default, list):
            raise TypeError("ListProperty can accept type: 'list'")

        super().__init__(name, default, required, tooltip, display_name, display_icon if display_icon else "fa fa-list-ul")
        self.height = height

    def render(self) -> RenderedProperty:
        rendered = RenderedProperty(
            props = { self.var_name: { "value": self.default, "required": self.required } },
            props_map = { self.name: self.name }
        )

        eid = f"node-input-{self.var_name}"
        rendered.elements.extend([
            hg.DIV(
                hg.LABEL(
                    hg.I(_class = self.display_icon), " ",
                    hg.SPAN(self.display_name)
                ),
                _class = "form-row",
                style = "margin-bottom: 0px;",
                **{ "for": f"{eid}-container", "title": self.tooltip }
            ),
            hg.DIV(
                hg.OL(
                    id = f"{eid}-container",
                    style = f"height:{self.height}px;"
                ),
                _class = f"form-row {eid}-container-row"
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

# -*- coding: utf-8 -*-
import htmlgenerator as hg
from typing import List
from ..widget import Widget, RenderedWidget


class Tab(Widget):
    def __init__(self, title:str, widgets:List[Widget], icon:str = "fa fa-cog"):
        """
        Class to create tab in Node-RED editor dialog

        Parameters
        ----------
        title: str, required
            title of tab
        widgets: List[Widget], required
            widgets to place in tab
        icon: str, default "fa fa-cog"
            icon of tab
        """
        super().__init__()

        self.__title, self.__icon = title, icon
        self.__widgets = widgets

    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def id(self) -> str:
        return f"tab-item-{self.title.lower()}"

    def render(self) -> RenderedWidget:
        elements = []
        rendered_tab = RenderedWidget(
            prepare = """
            tabs.addTab({
                id: '""" + self.id + """',
                iconClass: '""" + self.__icon + """',
                label: '""" + self.title + """'
            });
"""
        )

        for widget in self.__widgets:
            rendered_widget = widget.render()
            
            rendered_tab.props.update(rendered_widget.props)
            rendered_tab.props_map.update(rendered_widget.props_map)
            elements.extend(rendered_widget.elements)
            rendered_tab.prepare += rendered_widget.prepare
            rendered_tab.cancel += rendered_widget.cancel
            rendered_tab.save += rendered_widget.save

        rendered_tab.elements.extend([
            hg.DIV(
                *elements,
                id = f"tab-item-{self.title.lower()}",
                style = "display:none;"
            )
        ])

        return rendered_tab

class Tabs:
    def __init__(self, tabs:List[Tab]):
        self.__tabs = tabs

    def render(self) -> RenderedWidget:
        elements = []
        rendered_tabs = RenderedWidget(
            props = {}, props_map = {},
            prepare = """
            var tabs = RED.tabs.create({
                id: "tab-frame",
                onchange: (tab) => {
                    $("#tabs-content").children().hide();
                    $(`#${tab.id}`).show();
                    RED.tray.resize();
                }
            })
"""
        )
        
        for tab in self.__tabs:
            rendered_tab = tab.render()
            
            rendered_tabs.props.update(rendered_tab.props)
            rendered_tabs.props_map.update(rendered_tab.props_map)
            elements.extend(rendered_tab.elements)
            rendered_tabs.prepare += rendered_tab.prepare
            rendered_tabs.cancel += rendered_tab.cancel
            rendered_tabs.save += rendered_tab.save

        if len(self.__tabs) > 0:
            rendered_tabs.prepare += f"\n            tabs.activateTab('{self.__tabs[0].id}');"

        rendered_tabs.elements.extend([
            hg.DIV(
                hg.UL(
                    id = "tab-frame",
                    style = "min-width: 600px;"
                ),
                _class = "form-row"
            ),
            hg.DIV(
                *elements,
                id = "tabs-content",
                style = "min-height:calc(100% - 95px);"
            )
        ])

        return rendered_tabs

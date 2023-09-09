# -*- coding: utf-8 -*-
from typing import List
from .widget import Widget, RenderedWidget
from ...node.properties.property import Property
from ...node.properties import Input
from .ui.tab import Tab, Tabs
from .ui.divider import Divider


class Editor:
    def __init__(self, widgets:List[Widget]):
        self.__widgets = widgets

    def render(self) -> RenderedWidget:
        rendered_editor = RenderedWidget(
            props = {}, props_map = {}
        )
        
        # classify property, tab
        widgets:List[Widget] = []
        tab_widgets:List[Tab] = []
        for widget in self.__widgets:
            if isinstance(widget, (Property, Divider)):
                widgets.append(widget)
            else:
                tab_widgets.append(widget)

        # append Name property
        if len(widgets) > 0 or len(tab_widgets) > 0:
            widgets.insert(0, Divider())

        widgets.insert(0,
            Input("name", "", display_icon = "fa fa-tag", one_line = True)
        )
        if len(tab_widgets) > 0:
            widgets.append(Tabs(tab_widgets))

        for widget in widgets:
            rendered_widget = widget.render()

            rendered_editor.props.update(rendered_widget.props)
            rendered_editor.props_map.update(rendered_widget.props_map)
            rendered_editor.elements.extend(rendered_widget.elements)
            rendered_editor.prepare += rendered_widget.prepare
            rendered_editor.cancel += rendered_widget.cancel
            rendered_editor.save += rendered_widget.save

            del rendered_widget

        return rendered_editor

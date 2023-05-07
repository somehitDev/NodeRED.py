# -*- coding: utf-8 -*-
import os, json, noderedpy
from .._property import (
    InputProperty, ListProperty,
    SpinnerProperty, ComboBoxProperty, CodeProperty
)
from . import __path__


def package_json(node:"noderedpy._nodered.Node") -> str:
    with open(os.path.join(__path__[0], "template.json"), "r", encoding = "utf-8") as tr:
        tt = tr.read()

    return tt.replace(
        "{$node_name}", node.name
    )

def node_html(node:"noderedpy._nodered.Node") -> str:
    properties_html, properties_js, properties_js_prepare, properties_js_cancel, properties_js_save = [], [], [], [], []
    default_value = None
    for property in node.properties:
        if isinstance(property, InputProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <input type="text" id="node-input-{property.name}" style="width:100%;">
    </div>
""")
            default_value = f'"{property.default}"' if isinstance(property.default, str) else str(property.default)
        elif isinstance(property, ListProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row node-input-{property.name}-container-row">
        <ol id="node-input-{property.name}-container" style="height:{property.height}px;"></ol>
    </div>
""")
            properties_js_prepare.append('''
            $("#node-input-''' + property.name + '''-container").editableList({
                addItem: (container, idx, opt) => {
                    opt.idx = idx;
                    opt.value = opt.value ?? "";

                    container.css({ overflow: "hidden", display: "flex", "align-items": "center" });
                    $("<input>", { class: "input-list-item", type: "text", style:"flex:1;" }).val(opt.value).appendTo(container);
                },
                removable: true
            });

            for (var item of this.''' + property.name + ''') {
                $("#node-input-''' + property.name + '''-container").editableList("addItem", { value: item });
            }
''')
            properties_js_save.append('''
            this.''' + property.name + ''' = [];
            $("#node-input-''' + property.name + '''-container").editableList("items").each((_, item) => {
                this.''' + property.name + '''.push(item.find("input.input-list-item").val());
            });
''')
            default_value = str(property.default)
        elif isinstance(property, CodeProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row node-text-editor-row">
        <div style="height:{property.height}px;" class="node-text-editor" id="node-input-{property.name}"></div>
    </div>
""")
            if property.language:
                properties_js_prepare.append('''
            this.''' + property.name + '''Editor = RED.editor.createEditor({
                id: "node-input-''' + property.name + '''",
                mode: "ace/mode/''' + property.language + '''",
                value: this.''' + property.name + ''',
                focus: true
            });
''')
            else:
                properties_js_prepare.append('''
            this.''' + property.name + '''Editor = RED.editor.createEditor({
                id: "node-input-''' + property.name + '''",
                value: this.''' + property.name + ''',
                focus: true
            });
''')
            properties_js_cancel.append(f"""
            this.{property.name}Editor.destroy();
            delete this.{property.name}Editor;
""")
            properties_js_save.append(f"""
            $("#node-input-{property.name}").val(this.{property.name}Editor.getValue().trim());
            this.{property.name}Editor.destroy();
            delete this.{property.name}Editor;
""")
            default_value = f"`{property.default}`"
        elif isinstance(property, SpinnerProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <input type="text" id="node-input-{property.name}" style="width:calc(100% - 22px);">
    </div>
""")
            spinner_configs = []
            if property.min:
                spinner_configs.append(f"                min: {property.min},")
            if property.max:
                spinner_configs.append(f"                max: {property.max},")
            if property.step:
                spinner_configs.append(f"                step: {property.step}")

            properties_js_prepare.append('''
            $("#node-input-''' + property.name + '''").spinner({
                ''' + "\n".join(spinner_configs) + '''
            });
''')
            default_value = str(property.default)
        elif isinstance(property, ComboBoxProperty):
            options = "\n".join([
                f"""
            <option value="{item}">{item}</option>
"""
                for item in property.items
            ])
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <select id="node-input-{property.name}Select" style="width:100%;">
{options}
        </select>
        <input type="text" id="node-input-{property.name}" style="display:none;">
    </div>
""")
            properties_js_prepare.append('''
            $("#node-input-''' + property.name + '''Select").val(this.''' + property.name + ''');
''')
            properties_js_save.append('''
            $("#node-input-''' + property.name + '''").val($("#node-input-''' + property.name + ''';").val());
''')
            default_value = f'"{property.default}"' if isinstance(property.default, str) else str(property.default)

        if default_value:
            properties_js.append("            " + property.name + ': { value: ' + default_value + ' }')

    with open(os.path.join(__path__[0], "template.html"), "r", encoding = "utf-8") as tr:
        tt = tr.read()

    return tt.replace(
        "{$node_name}", node.name
    ).replace(
        "{$node_category}", node.category
    ).replace(
        "{$properties_html}", "".join(properties_html)
    ).replace(
        "{$properties_js}", ",\n".join(properties_js)
    ).replace(
        "{$properties_js_prepare}", "\n".join(properties_js_prepare)
    ).replace(
        "{$properties_js_cancel}", "\n".join(properties_js_cancel)
    ).replace(
        "{$properties_js_save}", "\n".join(properties_js_save)
    )

def node_js(node:"noderedpy._nodered.Node", cache_dir:str) -> str:
    with open(os.path.join(__path__[0], "template.js"), "r", encoding = "utf-8") as tr:
        tt = tr.read()

    return tt.replace(
        "{$node_name}", node.name
    ).replace(
        "{$node_properties}", str([ property.name for property in node.properties])
    ).replace(
        "{$cache_dir}", cache_dir
    )

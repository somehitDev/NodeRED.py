# -*- coding: utf-8 -*-
import os, noderedpy
from ..__property__ import (
    InputProperty, ListProperty,
    SpinnerProperty, CheckBoxProperty, ComboBoxProperty, CodeProperty,
    # FileProperty, TableProperty
)
from . import __path__


def package_json(node:"noderedpy.__nodered__.Node") -> str:
    with open(os.path.join(__path__[0], "template.json"), "r", encoding = "utf-8") as tr:
        tt = tr.read()

    tt = tt.replace(
        "{$node_name}", node.name
    ).replace(
        "{$node_version}", node.version
    ).replace(
        "{$node_description}", node.description
    ).replace(
        "{$node_author}", node.author
    )
    
    if node.keywords == []:
        tt = tt.replace(
            "{$node_keywords}", ""
        )
    else:
        tt = tt.replace(
            "{$node_keywords}", ", " + ", ".join([ f'"{keyword}"' for keyword in node.keywords ])
        )

    return tt

def node_html(node:"noderedpy.__nodered__.Node") -> str:
    properties_html, properties_js, properties_js_prepare, properties_js_cancel, properties_js_save = [], [], [], [], []
    default_value = None
    for property in node.properties:
        if isinstance(property, InputProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <input type="text" id="node-input-{property.var_name}" style="width:100%;">
    </div>
""")
            default_value = f'"{property.default}"' if isinstance(property.default, str) else str(property.default)
        elif isinstance(property, ListProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row node-input-{property.var_name}-container-row">
        <ol id="node-input-{property.var_name}-container" style="height:{property.height}px;"></ol>
    </div>
""")
            properties_js_prepare.append('''
            $("#node-input-''' + property.var_name + '''-container").editableList({
                addItem: (container, idx, opt) => {
                    opt.idx = idx;
                    opt.value = opt.value ?? "";

                    container.css({ overflow: "hidden", display: "flex", "align-items": "center" });
                    $("<input>", { class: "input-list-item", type: "text", style:"flex:1;" }).val(opt.value).appendTo(container);
                },
                removable: true
            });

            for (var item of node["''' + property.var_name + '''"]) {
                $("#node-input-''' + property.var_name + '''-container").editableList("addItem", { value: item });
            }
''')
            properties_js_save.append('''
            node["''' + property.var_name + '''"] = [];
            $("#node-input-''' + property.var_name + '''-container").editableList("items").each((_, item) => {
                node["''' + property.var_name + '''"].push(item.find("input.input-list-item").val());
            });
''')
            default_value = str(property.default)
        elif isinstance(property, CodeProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row node-text-editor-row">
        <div style="height:{property.height}px;" class="node-text-editor" id="node-input-{property.var_name}"></div>
    </div>
""")
            if property.language:
                properties_js_prepare.append('''
            node["''' + property.var_name + '''Editor"] = RED.editor.createEditor({
                id: "node-input-''' + property.var_name + '''",
                mode: "ace/mode/''' + property.language + '''",
                value: node["''' + property.var_name + '''"],
                focus: true
            });
''')
            else:
                properties_js_prepare.append('''
            node["''' + property.var_name + '''Editor"] = RED.editor.createEditor({
                id: "node-input-''' + property.var_name + '''",
                value: node["''' + property.var_name + '''"],
                focus: true
            });
''')
            properties_js_cancel.append(f"""
            node["{property.var_name}Editor"].destroy();
            delete node["{property.var_name}Editor"];
""")
            properties_js_save.append(f"""
            $("#node-input-{property.var_name}").val(node["{property.var_name}Editor"].getValue().trim());
            node["{property.var_name}Editor"].destroy();
            delete node["{property.var_name}Editor"];
""")
            default_value = f"`{property.default}`"
        elif isinstance(property, SpinnerProperty):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <input type="text" id="node-input-{property.var_name}" style="width:calc(100% - 22px);">
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
            $("#node-input-''' + property.var_name + '''").spinner({
                ''' + "\n".join(spinner_configs) + '''
            });
''')
            default_value = str(property.default)
        elif isinstance(property, CheckBoxProperty):
            properties_html.append(f"""
    <div class="form-row">
        <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
        <input type="checkbox" style="margin-left:10px;width:15px;height:15px;margin-bottom:5px;" id="node-input-{property.var_name}">
    </div>
""")
            default_value = "true" if property.default else "false"
        elif isinstance(property, ComboBoxProperty):
            options = "\n".join([
                f"""
            <option value="{item}">{item}</option>
"""
                for item in property.items
            ])
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <select id="node-input-{property.var_name}Select" style="width:100%;">
{options}
        </select>
        <input type="text" id="node-input-{property.var_name}" style="display:none;">
    </div>
""")
            properties_js_prepare.append('''
            $("#node-input-''' + property.var_name + '''Select").val($("#node-input-''' + property.var_name + '''").val());
''')
            properties_js_save.append('''
            $("#node-input-''' + property.var_name + '''").val($("#node-input-''' + property.var_name + '''Select").val());
''')
            default_value = f'"{property.default}"' if isinstance(property.default, str) else str(property.default)
#         elif isinstance(property, FileProperty):
#             properties_html.append(f"""
#     <div class="form-row" style="display:flex;flex-flow:row;align-items:center;">
#         <label style="width:auto;margin-bottom:0px;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
#         <input type="file" id="node-input-{property.name}" style="flex:1;">
#     </div>
# """)
#             default_value = f'"{property.default}"'
#         elif isinstance(property, TableProperty):
#             theader = "\n".join([ f"                <th>{column}</th>" for column in property.default.columns ])
#             properties_html.append(f"""
#     <div class="form-row" style="margin-bottom:0px;">
#         <label style="width:auto;"><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
#     </div>
#     <div class="form-row" style="display:flex;flex-flow:column;">
#         <table>
#             <thead>
# {theader}
#             </thead>
#             <tbody>
#             </tbody>
#         </table>
#     </div>
# """)

        if default_value:
            required = 'true' if property.required else 'false'
            properties_js.append('            "' + property.var_name + '": { value: ' + default_value + ', required: ' + required + ' }')

    with open(os.path.join(__path__[0], "template.html"), "r", encoding = "utf-8") as tr:
        tt = tr.read()

    return tt.replace(
        "{$node_name}", node.name
    ).replace(
        "{$node_category}", node.category
    ).replace(
        "{$node_icon}", f'"{node.icon}"' if node.icon else "null"
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

def node_js(node:"noderedpy.__nodered__.Node", cache_dir:str) -> str:
    with open(os.path.join(__path__[0], "template.js"), "r", encoding = "utf-8") as tr:
        tt = tr.read()

    return tt.replace(
        "{$node_name}", node.name
    ).replace(
        "{$node_properties}", str([ property.var_name for property in node.properties])
    ).replace(
        "{$cache_dir}", cache_dir
    )

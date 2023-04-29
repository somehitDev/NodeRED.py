# -*- coding: utf-8 -*-
import json, noderedpy


def package_json(node:"noderedpy._nodered.Node") -> str:
    return json.dumps({
        "name": node.name,
        "version": "1.0.0",
        "description": f"nodered.py {node.name} node",
        "author": "nodered.py",
        "keywords": [ "node-red" ],
        "node-red": {
            "nodes": {
                node.name: f"lib/{node.name}.js"
            }
        }
    }, indent = 4)

def node_html(node:"noderedpy._nodered.Node") -> str:
    properties_html, properties_js, properties_js_prepare, properties_js_cancel, properties_js_save = [], [], [], [], []
    for property in node.properties:
        if property.type in ( "str", "int", "float" ):
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row">
        <input type="text" id="node-input-{property.name}">
    </div>
""")
        elif property.type == "list":
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row node-input-{property.name}-container-row">
        <ol id="node-input-{property.name}-container" style="height:250px;"></ol>
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
        else:
            properties_html.append(f"""
    <div class="form-row" style="margin-bottom:0px;">
        <label><i class="{property.display_icon}"></i> <span>{property.display_name}</span></label>
    </div>
    <div class="form-row node-text-editor-row">
        <div style="height:250px;" class="node-text-editor" id="node-input-{property.name}"></div>
    </div>
""")
            properties_js_prepare.append('''
            this.''' + property.name + '''Editor = RED.editor.createEditor({
                id: "node-input-''' + property.name + '''",
                mode: "ace/mode/json",
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
                                   
        if property.default_value:
            default_value = f'"{property.default_value}"' if property.type == "str" else f"`{json.dumps(property.default_value, indent = 4)}`" if property.type == "dict" else str(property.default_value)
        else:
            default_value = '""' if property.type == "str" else "[]" if property.type == "list" else '"{}"' if property.type == "dict" else "0"

        properties_js.append("            " + property.name + ': { value: ' + default_value + ' }')

    return '''
<script type="text/html" data-template-name="''' + node.name + '''">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> <span>Name</span></label>
        <input type="text" id="node-input-name" style="width:calc(100% - 105px);">
    </div>
    <hr>
    ''' + "".join(properties_html) + '''
</script>

<script type="text/javascript">
    RED.nodes.registerType("''' + node.name + '''", {
        category: "''' + node.category + '''",
        color: "#FDD0A2",
        defaults: {
            name: { value: "" },
''' + ",\n".join(properties_js) + '''
        },
        inputs: 1, outputs: 1,
        icon: "function.png",
        label: function() {
            return this.name;
        },
        oneditprepare: function() {
''' + "\n".join(properties_js_prepare) + '''
        },
        oneditcancel: function() {
''' + "\n".join(properties_js_cancel) + '''
        },
        oneditsave: function() {
''' + "\n".join(properties_js_save) + '''
        }
    });
</script>
'''

def node_js(node:"noderedpy._nodered.Node", port:int) -> str:
    return '''
let messageCache = {};
    
module.exports = function(RED) {
    function fnNode(config) {
        var node = this;
        RED.nodes.createNode(this, config);

        this.status({ fill: "blue", shape: "dot", text: "Ready" });
        this.on("input", (message) => {
            messageCache._msgid = message._msgid;
            delete message._msgid;

            var reqToSend = null;
            if (message.req != undefined && typeof(message.req) == "object") {
                messageCache.req = message.req;

                reqToSend = {
                    payload: message.req.payload,
                    body: message.req.body,
                    cookie: message.req.cookie,
                    header: {}
                };
                for (var idx = 0; idx < message.req.rawHeaders.length / 2; idx++) {
                    reqToSend.header[message.req.rawHeaders[idx * 2]] = message.req.rawHeaders[idx * 2 + 1];
                }

                message.req = reqToSend;
            }
            if (message.res != undefined && typeof(message.res) == "object") {
                messageCache.res = message.res;
                delete message.res;            
            }

            var configToSend = {};
            for (var name of ''' + str([ property.name for property in node.properties]) + ''') {
                var config_item = config[name];
                if (typeof(config_item) == "string" && (config_item.startsWith("{") && config_item.endsWith("}"))) {
                    config_item = JSON.parse(config_item);
                }
                configToSend[name] = config_item;
            }

            node.status({ fill: "green", shape: "dot", text: "Running" });

            try {
                fetch("http://127.0.0.1:''' + str(port) + '''/nodes/''' + node.name + '''", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        props: configToSend, msg: message
                    })
                }).then(async (resp) => {
                    var message = await resp.json();
                    const state = message.state;
                    delete message.state;

                    if (state == "success") {
                        message._msgid = messageCache._msgid;
                        if (messageCache.req != undefined) {
                            message.req = messageCache.req;
                        }
                        if (messageCache.res != undefined) {
                            message.res = messageCache.res;
                        }

                        node.send(message);
                        node.status({ fill: "green", shape: "dot", text: "Finished" });
                    }
                    else {
                        node.error(message.message);
                        node.status({ fill: "red", shape: "dot", text: "Stopped, see debug panel" });
                    }
                });
            }
            catch (err) {
                node.error(err.message);
                node.status({ fill: "red", shape: "dot", text: "Stopped, see debug panel" });
            }
        });
    }

    RED.nodes.registerType("''' + node.name + '''", fnNode);
}
'''

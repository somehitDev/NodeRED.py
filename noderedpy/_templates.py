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
    properties_html, properties_js = [], []
    for property in node.properties:
        properties_html.append(f"""
    <div class="form-row">
        <label for="node-input-{property.name}"><i class="fa fa-tag"></i> <span>{property.name.capitalize()}</span></label>
        <input type="text" id="node-input-{property.name}" style="width:calc(100% - 105px);">
    </div>
""")
        if property.default_value:
            default_value = f'"{property.default_value}"' if property.type == "str" else f"{property.default_value}"
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
        label: () => this.name
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
                configToSend[name] = config[name];
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

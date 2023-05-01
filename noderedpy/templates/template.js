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
            for (var name of {$node_properties}) {
                var config_item = config[name];
                if (typeof(config_item) == "string" && (config_item.startsWith("{") && config_item.endsWith("}"))) {
                    config_item = JSON.parse(config_item);
                }
                configToSend[name] = config_item;
            }

            node.status({ fill: "green", shape: "dot", text: "Running" });

            try {
                fetch("http://127.0.0.1:{$port}/nodes/{$node_name}", {
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

    RED.nodes.registerType("{$node_name}", fnNode);
}
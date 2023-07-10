const fs = require("fs"), path = require("path");

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
                    reqToSend.header[message.req.rawHeaders[idx * 2]] = message.req.rawHeaders[idx * 2 + 1].replaceAll('"', "'");
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

            const inpFile = path.join("{$cache_dir}", "input.json");
            const outFile = path.join("{$cache_dir}", "output.json");
            const messageFile = path.join("{$cache_dir}", "message.json");

            // remove if outFile exists before run
            if (fs.existsSync(outFile)) {
                fs.unlinkSync(outFile);
            }

            // send inputs to python
            fs.writeFileSync(inpFile, JSON.stringify({
                name: "{$node_name}",
                props: configToSend, msg: message
            }, null, "    "));

            // wait until job done
            var resp = null;
            while (true) {
                if (fs.existsSync(messageFile)) {
                    try {
                        var resp_msg = JSON.parse(fs.readFileSync(messageFile));
                        if (resp_msg.name == "{$node_name}") {
                            fs.unlinkSync(messageFile);

                            if (resp_msg.status != undefined) {
                                node.status(resp_msg.status);
                            }
                            if (resp_msg.log != undefined) {
                                node.log(resp_msg.log.join(" "));
                            }
                            if (resp_msg.warn != undefined) {
                                node.warn(resp_msg.warn.join(" "));
                            }
                            if (resp_msg.error != undefined) {
                                node.error(resp_msg.error.join(" "));
                            }
                        }
                    }
                    catch {
                        continue;
                    }
                }

                if (fs.existsSync(outFile)) {
                    try {
                        resp = JSON.parse(fs.readFileSync(outFile));
                        if (resp.name == "{$node_name}") {
                            fs.unlinkSync(outFile);
                            break;
                        }
                    }
                    catch {
                        continue;
                    }
                }
            }

            // get result ans parse
            try {
                const state = resp.state;
                delete resp.state;

                if (state == "success") {
                    resp._msgid = messageCache._msgid;
                    if (messageCache.req != undefined) {
                        resp.req = messageCache.req;
                    }
                    if (messageCache.res != undefined) {
                        resp.res = messageCache.res;
                    }

                    node.send(resp);
                    node.status({ fill: "green", shape: "dot", text: "Finished" });
                }
                else {
                    node.error(resp.message);
                    node.status({ fill: "red", shape: "dot", text: "Stopped, see debug panel" });
                }
            }
            catch (err) {
                node.error(err.message);
                node.status({ fill: "red", shape: "dot", text: "Stopped, see debug panel" });
            }
        });
    }

    RED.nodes.registerType("{$node_name}", fnNode);
}
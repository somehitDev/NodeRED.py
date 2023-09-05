# -*- coding: utf-8 -*-
import os
from typing import List


def node_js(name:str, prop_names:List[str], cache_dir:os.PathLike):
    return """
const fs = require("fs"), path = require("path");

let messageCache = {};

function $sleep(ms) {
    const wakeUpTime = Date.now() + ms;
    while (Date.now() < wakeUpTime) {}
}

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
                    header: {}
                };
                try {
                    reqToSend.payload = JSON.parse(message.req.payload);
                }
                catch {
                    reqToSend.payload = message.req.payload;
                }
                try {
                    reqToSend.body = JSON.parse(message.req.body);
                }
                catch {
                    reqToSend.body = message.req.body;
                }
                try {
                    reqToSend.cookie = JSON.parse(message.req.cookie);
                }
                catch {
                    reqToSend.cookie = message.req.cookie;
                }

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
            for (var name of {$prop_names}) {
                var config_item = config[name];
                if (typeof(config_item) == "string" && (config_item.startsWith("{") && config_item.endsWith("}"))) {
                    config_item = JSON.parse(config_item);
                }
                configToSend[name.substring(7)] = config_item;
            }

            node.status({ fill: "green", shape: "dot", text: "Running" });

            const inpFile = path.join("{$cache_dir}", "node_input.json");
            const outFile = path.join("{$cache_dir}", "node_output.json");
            const messageFile = path.join("{$cache_dir}", "node_message.json");

            // remove if outFile exists before run
            if (fs.existsSync(outFile)) {
                fs.unlinkSync(outFile);
            }

            // send inputs to python
            fs.writeFileSync(inpFile, JSON.stringify({
                name: "{$name}",
                props: configToSend, msg: message
            }, null, "    "));

            // wait until job done
            var resp = null;
            while (true) {
                if (fs.existsSync(messageFile)) {
                    try {
                        var resp_msg = JSON.parse(fs.readFileSync(messageFile));
                        if (resp_msg.name == "{$name}") {
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
                        if (resp.name == "{$name}") {
                            fs.unlinkSync(outFile);
                            break;
                        }
                    }
                    catch {
                        // $sleep(1000);
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
                    node.error(`
${resp.message}`);
                    console.log(`============================= error
`);
                    node.status({ fill: "red", shape: "dot", text: "Stopped, see debug panel" });
                }
            }
            catch (err) {
                node.error(`
${err.message}`);
                console.log(`============================= error
`);
                node.status({ fill: "red", shape: "dot", text: "Stopped, see debug panel" });
            }
        });
    }

    RED.nodes.registerType("{$name}", fnNode);
}
""".replace("{$name}", name).replace("{$prop_names}", str(prop_names))\
    .replace("{$cache_dir}", cache_dir)

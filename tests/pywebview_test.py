# -*- coding: utf-8 -*-
"""
requirements: pywebview>=3.7.2
"""

import os, webview
from noderedpy import (
    RED, Node,
    InputProperty, ListProperty, DictProperty
)
from noderedpy.decorator import register

__dirname = os.path.dirname(os.path.realpath(__file__))
if __name__ == "__main__":
    class TotalApp:
        count = 0

        @register("test", properties = [
            InputProperty("test_prop", "1234"),
            ListProperty("list_prop", [ 1, 2, 3, 4 ]),
            DictProperty("dict_prop", { "a": 1 })
        ])
        def test(node:Node, props:dict, msg:dict) -> dict:
            TotalApp.count += 1

            print(props)
            print(msg)

            msg["payload"] = TotalApp.count

            return msg

    red = RED(
        os.path.join(__dirname, ".node-red-pywebview"),
        os.path.join(__dirname, "node_red_dir"),
        "/node-red",
        port = 1880,
        editor_theme = {
            "projects": {
                "enabled": False
            }
        }
    )

    webview.initialize()
    win = webview.create_window("Node-RED.py pywebview")
    win.events.closing += red.stop

    webview.start(lambda: red.start(callback = lambda: win.load_url(f"http://127.0.0.1:{red.port}{red.admin_root}"), start_browser = False), debug = True)

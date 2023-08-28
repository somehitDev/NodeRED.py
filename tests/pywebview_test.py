# -*- coding: utf-8 -*-
"""
requirements: pywebview>=3.7.2
"""

import os, webview
from noderedpy import (
    RED, REDBuilder, Auth, Node,
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
        
    # get RED object from builder
    red = REDBuilder()\
        .set_user_dir(os.path.join(__dirname, ".node-red-pywebview"))\
        .set_node_red_dir(os.path.join(__dirname, "node_red_dir"))\
        .set_admin_root("/node-red")\
        .set_port(1880)\
        .set_remote_access(False).build()

    # # init RED object directly
    # red = RED(
    #     os.path.join(__dirname, ".node-red-pywebview"),
    #     os.path.join(__dirname, "node_red_dir"),
    #     "/node-red",
    #     port = 1880,
    #     editor_theme = {
    #         "projects": {
    #             "enabled": False
    #         }
    #     }
    # )

    # set editor theme
    red.editor_theme.palette.editable = False
    red.editor_theme.projects.enabled = False

    # add auths
    red.node_auths.append(
        Auth(username = "node-red-py", password = "p@ssword")
    )

    webview.initialize()
    win = webview.create_window("Node-RED.py pywebview")
    win.events.closing += lambda: red.stop()

    webview.start(lambda: red.start(callback = lambda: win.load_url(f"http://127.0.0.1:{red.port}{red.admin_root}"), start_browser = False), debug = True)

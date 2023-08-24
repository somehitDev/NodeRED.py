# -*- coding: utf-8 -*-
import os
from noderedpy import (
    REDBuilder, Auth, Node,
    InputProperty, ListProperty, DictProperty, CodeProperty,
    SpinnerProperty, CheckBoxProperty, ComboBoxProperty
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
        
        @register(
            "property-test", author = "oyajiDev", version = "0.1.0", description = "test for multi properties",
            icon = "database.png",
            properties = [
                InputProperty("input_prop", "input property"),
                ListProperty("list_prop", [ "list", "property" ], 150),
                DictProperty("dict_prop", { "dict": "property" }, 100),
                SpinnerProperty("spinner_prop", 1),
                CheckBoxProperty("chkbox_prop", True),
                ComboBoxProperty("cbox_prop", [ "combobox", "property" ]),
                CodeProperty("code_prop", "print(1234)", "python")
            ]
        )
        def property_test(node:Node, props:dict, msg:dict) -> dict:
            node.status("grey", "ring", "status test")
            node.log("123", "456", "789")
            node.warn("123", "456", "789")
            node.error("123", "456", "789")

            print(props, msg)
            return msg
        
        def test2(self, node:Node, props:dict, msg:dict) -> dict:
            print(self.count, msg["payload"])

            return msg

    # get RED object from builder
    red = REDBuilder()\
        .set_user_dir(os.path.join(__dirname, ".node-red"))\
        .set_node_red_dir(os.path.join(__dirname, "node_red_dir"))\
        .set_admin_root("/node-red")\
        .set_port(1880)\
        .set_remote_access(False).build()
    
    # set editor theme
    red.editor_theme.palette.editable = False
    red.editor_theme.projects.enabled = False

    # add auths
    red.node_auths.append(
        Auth(username = "node-red-py", password = "p@ssword")
    )

    # red = RED(
    #     os.path.join(__dirname, ".node-red"),
    #     os.path.join(__dirname, "node_red_dir"),
    #     "/node-red", 
    #     port = 1880,
    #     editor_theme = {
    #         "palette": {
    #             "editable": False
    #         },
    #         "projects": {
    #             "enabled": False
    #         }
    #     },
    #     auths = [
    #         { "username": "node-red-py", "password": "p@ssword" }
    #     ]
    # )

    app = TotalApp()
    red.register(app.test2, "test2")

    red.start(debug = True, start_browser = False)

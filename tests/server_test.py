# -*- coding: utf-8 -*-
import os
from noderedpy import (
    RED,
    InputProperty, ListProperty, DictProperty,
    SpinnerProperty, ComboBoxProperty, CodeProperty
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
        def test(props:dict, msg:dict) -> dict:
            TotalApp.count += 1

            print(props)
            print(msg)

            msg["payload"] = TotalApp.count

            return msg
        
        @register("property-test", properties = [
            InputProperty("input_prop", "input property"),
            ListProperty("list_prop", [ "list", "property" ], 150),
            DictProperty("dict_prop", { "dict": "property" }, 100),
            SpinnerProperty("spinner_prop", 1),
            ComboBoxProperty("cbox_prop", [ "combobox", "property" ], "property"),
            CodeProperty("code_prop", "print(1234)", "python")
        ])
        def property_test(props:dict, msg:dict) -> dict:
            print(props, msg)
            return msg
        
        def test2(self, pros:dict, msg:dict) -> dict:
            print(self.count, msg["payload"])

            return msg

    # server = Server(
    #     RED(
    #         os.path.join(__dirname, ".node-red"),
    #         os.path.join(__dirname, "node_red_dir"),
    #         "/node-red", 1880
    #     )
    # )
    red = RED(
        os.path.join(__dirname, ".node-red"),
        os.path.join(__dirname, "node_red_dir"),
        "/node-red", 1880
    )

    app = TotalApp()
    # server.register(app.test2, "test2")
    red.register(app.test2, "test2")

    # server.start(1881, show_browser = False)
    red.start(True)

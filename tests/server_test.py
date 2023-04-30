# -*- coding: utf-8 -*-
import os
from noderedpy import (
    RED, Server,
    InputProperty, ListProperty, DictProperty,
    SpinnerProperty, ComboBoxProperty
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
            ListProperty("list_prop", [ "list", "property" ]),
            DictProperty("dict_prop", { "dict": "property" }),
            SpinnerProperty("spinner_prop", 1),
            ComboBoxProperty("cbox_prop", [ "combobox", "property" ], "property")
        ])
        def property_test(props:dict, msg:dict) -> dict:
            print(props, msg)
            return msg
        
        def test2(self, pros:dict, msg:dict) -> dict:
            print(self.count, msg["payload"])

            return msg

    server = Server(
        RED(
            os.path.join(__dirname, ".node-red"),
            "/node-red", 1880
        )
    )

    app = TotalApp()
    server.register(app.test2, "test2")

    server.start(1881, show_browser = False)

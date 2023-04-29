# -*- coding: utf-8 -*-
import os
from noderedpy import NodeProperty, RED, Server
from noderedpy.decorator import register

__dirname = os.path.dirname(os.path.realpath(__file__))
if __name__ == "__main__":
    class TotalApp:
        count = 0

        @register("test", properties = [
            NodeProperty("test_prop", "str", "1234"),
            NodeProperty("list_prop", "list", [ 1, 2, 3, 4 ]),
            NodeProperty("dict_prop", "dict", { "a": 1 })
        ])
        def test(props:dict, msg:dict) -> dict:
            TotalApp.count += 1

            print(props)
            print(msg)

            msg["payload"] = TotalApp.count

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

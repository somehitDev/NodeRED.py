# -*- coding: utf-8 -*-
import os
from noderedpy import NodeProperty, RED, StandaloneServer
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

    StandaloneServer(
        RED(
            os.path.join(__dirname, ".node-red-standalone"),
            "/node-red", 1880
        )
    ).start("NodeRED.py standalone", debug = True)

# -*- coding: utf-8 -*-
import os
from noderedpy import (
    RED, StandaloneServer,
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

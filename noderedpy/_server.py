# -*- coding: utf-8 -*-
import os, sys, json, shutil, asyncio
from glob import glob
from typing import List, Type
from types import MethodType
from aiohttp import web
from ._nodered import RED, Node
from ._property import Property


class Server(web.Application):
    """
    Server to communicate with Node-RED
    """
    registered_nodes:List[Node] = []

    def __init__(self, node_red:RED):
        """
        Initialize Server to communicate with Node-RED

        Parameters
        ----------
        node_red: RED, required
            Node-RED settings
        """
        super().__init__()

        self.__red = node_red
        # setup Node-RED
        node_red.start_for_ready()

    async def __call_node(self, req:web.Request, node_name:str):
        node = list(filter(lambda n: n.name == node_name, Server.registered_nodes))[0]

        data = await req.json()
        return web.Response(
            text = json.dumps(node.run(data["props"], data["msg"])),
            content_type = "application/json"
        )

    def __on_started(self):
        if self.__show_browser:
            import webbrowser
            webbrowser.open_new(f"http://127.0.0.1:{self.__red.port}/node-red")

        if self.__start_callback:
            self.__start_callback()


    def register(self, node_func:MethodType, name:str, category:str = "nodered_py", properties:List[Property] = []):
        """
        Function to register Node function

        Parameters
        ----------
        node_func: MethodType, required
            Node function to register
        name: str, required
            name of Node to register
        category: str, default nodered_py
            category of Node
        properties: List[noderedpy._property.Property]
            propertis of Node
        """
        node = Node(name if name.startswith("nodered-py") else f"nodered-py-{name}", category, properties, node_func)
        Server.registered_nodes.append(node)

    def start(self, port:int, show_browser:bool = True, callback:MethodType = None):
        """
        Start Server

        Parameters
        ----------
        port: int, required
            port for Server
        show_browser: bool, default True
            show browser when started or not
        callback: MethodType, default None
            callback when Server started
        """
        self.__port, self.__show_browser, self.__start_callback = port, show_browser, callback
        self.__red.start(callback = self.__on_started, server = Server)

        # remove existing nodes
        for node_dir in glob(os.path.join(self.__red.user_dir, "node_modules", "nodered-py-*")):
            shutil.rmtree(node_dir)

        # create nodes
        for node in Server.registered_nodes:
            node.create(self.__red.user_dir, port)

        # map nodes to route
        self.add_routes([
            web.get("", lambda _: web.HTTPFound(f"http://127.0.0.1:{self.__red.port}/node-red")),
            web.post("/nodes/{node_name}", lambda req: self.__call_node(req, req.match_info["node_name"]))
        ])

        # start server
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = loop.create_server(self.make_handler(), host = "127.0.0.1", port = port)
        loop.run_until_complete(server)
        loop.run_forever()

    def stop(self):
        """
        Stop Server
        """
        import psutil, signal

        self.__red.stop()

        killed = False
        for process in psutil.process_iter():
            try:
                for conns in process.connections(kind = "inet"):
                    if conns.laddr.port == self.__port:
                        process.send_signal(signal.SIGTERM)
                        killed = True
                        break
            except psutil.AccessDenied:
                pass

            if killed:
                break

class StandaloneServer:
    """
    Server to Communicate with Node-RED and webview
    """
    def __init__(self, node_red:RED):
        """
        Initialize Server to communicate with Node-RED

        Parameters
        ----------
        node_red: RED, required
            Node-RED settings
        """
        self.__server = Server(node_red)
        self.__red = node_red

    def register(self, node_func:MethodType, name:str, category:str = "nodered_py", properties:List[Property] = []):
        """
        Function to register Node function

        Parameters
        ----------
        node_func: MethodType, required
            Node function to register
        name: str, required
            name of Node to register
        category: str, default nodered_py
            category of Node
        properties: List[noderedpy._property.Property]
            propertis of Node
        """
        self.__server.register(node_func, name, category, properties)

    def start(self, title:str, width:int = 1000, height:int = 650, x:int = None, y:int = None, debug:bool = False, port:int = 1881, default_root:str = None):
        """
        Start Server and show webview

        Parameters
        ----------
        title: str, required
            title of webview window
        width: int, default 1000
            default width of webview window
        height: int, default 650
            default height of webview window
        x: int, default None
            default x location of webview window
        y: int, default None
            default y location of webview window
        debug: bool, default False
            debug(devtools) or not
        port: int, default 1881
            port for Server
        default_root: str, default None
            default url root to show
            if None, use admin_root of Node-RED settings
        """
        default_root = self.__red.admin_root if default_root is None else default_root
        if not default_root.startswith("/"):
            raise ValueError("default_root must startswith '/'!")

        import webview

        webview.initialize("cocoa" if sys.platform == "darwin" else "cef" if sys.platform == "win32" else "qt")
        win = webview.create_window(title, width = width, height = height, x = x, y = y)
        win.events.closing += self.__server.stop

        webview.start(lambda: self.__server.start(port, False, lambda: win.load_url(f"http://127.0.0.1:{self.__red.port}{default_root}")), debug = debug)

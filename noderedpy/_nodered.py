# -*- coding: utf-8 -*-
import os, sys, subprocess, threading, traceback, noderedpy
from types import MethodType
from typing import Type, Literal, Any, List
from ._templates import package_json, node_html, node_js
from . import __path__


class RED:
    """
    Node-RED manager class
    """
    def __init__(self, user_dir:str, admin_root:str, port:int = 1880, show_default_category:bool = True):
        """
        Set configs of Node-RED and setup

        Parameters
        ----------
        user_dir: str, required
            userDir of Node-RED settings
        admin_root: str, required
            httpAdminRoot of Node-RED settings
        port: int, default 1880
            port of Node-RED server
        show_default_category: bool, default True
            show default categories of Node-RED or not
        """
        self.user_dir, self.admin_root, self.port, self.show_default_category =\
            user_dir, admin_root, port, show_default_category

        # setup Node-RED starter
        subprocess.call(
            [ "npm", "install" ],
            stdout = subprocess.DEVNULL,
            cwd = os.path.join(__path__[0], "node-red-starter")
        )

    # default started callback
    def __on_started(self, callback:MethodType = None):
        while True:
            if os.path.exists(self.__started_file):
                break

        callback()

    def start(self, wait:bool = False, debug:bool = True, callback:MethodType = None, server:Type["noderedpy._server.Server"] = None):
        """
        Start Node-RED server

        Parameters
        ----------
        wait: bool, default False
            wait for Node-RED server process of not
        debug: bool, default True
            show outputs on console or not
        callback: MethodType, default None
            callback when Node-RED server started
        server: Type[noderedpy._server.Server], default None
            server for setup "user category"
        """

        # set started flag file
        self.__started_file = os.path.join(__path__[0], "node-red-starter", "started")
        # kill if process listen on port
        self.stop()

        # map callback
        if callback:
            threading.Thread(target = self.__on_started, args = (callback,), daemon = True).start()

        # set subprocess args
        args = [
            "node",
            "index.js",
            f"--user-dir={self.user_dir}",
            f"--admin-root={self.admin_root}",
            f"--port={self.port}",
            f"--show-default-category={'true' if self.show_default_category else 'false'}"
        ]
        if server:
            args.append(
                f"--user-category={','.join(list(set([ node.category for node in server.registered_nodes ])))}"
            )

        # run Node-RED server
        proc = subprocess.Popen(
            args, shell = False, stdout = sys.stdout if debug else subprocess.DEVNULL,
            cwd = os.path.join(__path__[0], "node-red-starter")
        )
        if wait:# wait if flag is True
            proc.wait()

    def start_for_ready(self):
        """
        Start Node-RED for setup default userDir
        """
        def on_started():
            os.remove(self.__started_file)
            self.__stop()

        self.start(True, False, on_started)

    def __stop(self):
        import psutil, signal

        killed = False
        for process in psutil.process_iter():
            try:
                for conns in process.connections(kind = "inet"):
                    if conns.laddr.port == self.port:
                        process.send_signal(signal.SIGTERM)
                        killed = True
                        break
            except psutil.AccessDenied:
                pass

            if killed:
                break

    def stop(self):
        """
        Stop Node-RED server
        """
        if os.path.exists(self.__started_file):
            os.remove(self.__started_file)

        self.__stop()


class NodeProperty:
    """
    Property for Node function
    """
    def __init__(self, name:str, type:Literal["str", "int", "float", "list", "dict"], default_value:Any = None, required:bool = False, display_icon:str = None):
        """
        Property information for Node function

        Parameters
        ----------
        name: str, required
            name of Property
        type: Literal["str", "int", "float"], required
            type of Property
        default_value: Any, default None
            default value of Property
        required: bool, default False
            set Property is required or not
        display_icon: str, default None
            icon for Node-RED node display
        """
        if " " in name.strip():
            raise NameError("Property name cannot contain space!")
        
        if not type in ("str", "int", "float", "list", "dict"):
            raise TypeError("Currently supported types: [ 'str', 'int', 'float', 'list', 'dict' ]")
        
        if default_value is not None and not isinstance(default_value, ( str, int, float, list, dict )):
            raise TypeError("Currently supported value types: [ str, int, float, list, dict ]")

        self.name, self.type, self.default_value, self.required =\
            name, type, default_value, required
        
        if display_icon is None:
            if type in ( "int", "float" ):
                self.display_icon = "fa fa-sort-numeric-asc"
            elif type == "str":
                self.display_icon = "fa fa-font"
            elif type == "list":
                self.display_icon = "fa fa-list"
            elif type == "dict":
                self.display_icon = "fa fa-code"
        else:
            self.display_icon = display_icon
        
    @property
    def display_name(self) -> str:
        return " ".join([
            item.capitalize()
            for item in self.name.split("_")
        ])

class Node:
    def __init__(self, name:str, category:str, properties:List[NodeProperty], node_func:MethodType):
        if " " in name.strip():
            raise NameError("Node name cannot contain spaces!")
        
        if "-" in category.strip() or "," in category.strip():
            raise NameError("Category cannot contain '-' or ','!")

        self.name, self.category, self.properties =\
            name, category, properties
        
        self.__node_func = node_func

    def create(self, node_red_user_dir:str, port:int):
        node_dir = os.path.join(node_red_user_dir, "node_modules", self.name)
        os.makedirs(os.path.join(node_dir, "lib"))

        with open(os.path.join(node_dir, "package.json"), "w", encoding = "utf-8") as pjw:
            pjw.write(package_json(self))

        with open(os.path.join(node_dir, "lib", f"{self.name}.html"), "w", encoding = "utf-8") as nhw:
            nhw.write(node_html(self))

        with open(os.path.join(node_dir, "lib", f"{self.name}.js"), "w", encoding = "utf-8") as njw:
            njw.write(node_js(self, port))

    def run(self, props:dict, msg:dict) -> dict:
        print(f"{self.name} started\n===================================")
        try:
            resp = self.__node_func(props, msg)
            print("============================= ended\n")

            resp.update({ "state": "success" })

            return resp
        except:
            print("============================= error\n")
            return { "state": "fail", "message": traceback.format_exc() }

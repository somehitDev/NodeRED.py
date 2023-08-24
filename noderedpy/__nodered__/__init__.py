# -*- coding: utf-8 -*-
import os, sys, subprocess, shutil, json, traceback
from types import MethodType
from typing import List, Literal
from glob import glob
from ..templates import package_json, node_html, node_js
from ..__property__ import Property
from .theme import REDTheme
from .auth import AuthCollection
from .. import __path__


class RED:
    """
    Node-RED manager class
    """
    registered_nodes:List["Node"] = []

    def __init__(self, user_dir:str, node_red_dir:str, admin_root:str, node_root:str, port:int, default_flow:str, remote_access:bool, default_category_visible:bool):
        self.user_dir, self.admin_root, self.node_root, self.port, self.default_flow, self.remote_access, self.default_category_visible, self.__editor_theme, self.__node_auths =\
            user_dir, admin_root, node_root, port, default_flow, remote_access, default_category_visible, REDTheme(), AuthCollection()
        self.__temp_dir, self.__node_dir =\
            os.path.join(__path__[0], ".temp"), os.path.join(__path__[0], ".nodejs")

        if not self.admin_root.startswith("/"):
            raise SyntaxError("`admin_root` must starts with '/'!")

        if not self.node_root.startswith("/"):
            raise SyntaxError("`node_root` must starts with '/'!")

        # check node.js exists
        try:
            subprocess.call(
                [ "npm.cmd" if sys.platform == "win32" else "npm", "--version" ],
                stdout = subprocess.DEVNULL,
                stderr = subprocess.STDOUT
            )
            self.__npm_path = "npm.cmd" if sys.platform == "win32" else "npm"
            self.__node_path = "node.exe" if sys.platform == "win32" else "node"
        except FileNotFoundError:
            if not os.path.exists(self.__node_dir):
                import platform, wget, zipfile, tarfile

                node_version = "18.16.1"
                if not os.path.exists(self.__temp_dir):
                    os.mkdir(self.__temp_dir)

                if sys.platform == "win32":
                    node_bin_zip = os.path.join(self.__temp_dir, "node.zip")
                    if platform.architecture()[0] == "32bit":
                        wget.download(f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-win-x86.zip", node_bin_zip)
                        zipfile.ZipFile(node_bin_zip).extractall(self.__temp_dir)
                        shutil.move(os.path.join(self.__temp_dir, f"node-v{node_version}-win-x86"), self.__node_dir)
                    else:
                        wget.download(f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-win-x64.zip", node_bin_zip)
                        zipfile.ZipFile(node_bin_zip).extractall(self.__temp_dir)
                        shutil.move(os.path.join(self.__temp_dir, f"node-v{node_version}-win-x64"), self.__node_dir)

                    self.__npm_path = os.path.join(self.__node_dir, "npm.exe")
                    self.__node_path = os.path.join(self.__node_dir, "node.exe")
                elif sys.platform == "darwin":
                    node_bin_zip = os.path.join(self.__temp_dir, "node.tar.gz")
                    if platform.processor() == "arm":
                        wget.download(f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-darwin-arm64.tar.gz", node_bin_zip)
                        with tarfile.open(node_bin_zip, "r", encoding = "utf-8") as nbzr:
                            nbzr.extractall(self.__temp_dir)

                        shutil.move(os.path.join(self.__temp_dir, f"node-v{node_version}-darwin-arm64"), self.__node_dir)
                    else:
                        wget.download(f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-darwin-x64.tar.gz", node_bin_zip)
                        with tarfile.open(node_bin_zip, "r", encoding = "utf-8") as nbzr:
                            nbzr.extractall(self.__temp_dir)

                        shutil.move(os.path.join(self.__temp_dir, f"node-v{node_version}-darwin-x64"), self.__node_dir)

                    self.__npm_path = os.path.join(self.__node_dir, "bin", "npm")
                    self.__node_path = os.path.join(self.__node_dir, "bin", "node")
                else:
                    node_bin_zip = os.path.join(self.__temp_dir, "node.tar.xz")
                    if platform.processor() == "arm":
                        wget.download(f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-linux-armv7l.tar.xz", node_bin_zip)
                        with tarfile.open(node_bin_zip, "r", encoding = "utf-8") as nbzr:
                            nbzr.extractall(self.__temp_dir)

                        shutil.move(os.path.join(self.__temp_dir, f"node-v{node_version}-linux-armv7l"), self.__node_dir)
                    else:
                        wget.download(f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-linux-x64.tar.xz", node_bin_zip)
                        with tarfile.open(node_bin_zip, "r", encoding = "utf-8") as nbzr:
                            nbzr.extractall(self.__temp_dir)

                        shutil.move(os.path.join(self.__temp_dir, f"node-v{node_version}-linux-x64"), self.__node_dir)

                shutil.rmtree(self.__temp_dir)

            self.__npm_path = os.path.join(self.__node_dir, "bin", "npm.cmd" if sys.platform == "win32" else "npm")
            self.__node_path = os.path.join(self.__node_dir, "bin", "node.exe" if sys.platform == "win32" else "node")
        
        # set node_red_dir
        if node_red_dir is None:
            self.node_red_dir = os.path.join(__path__[0], "node-red-starter")
        else:
            self.node_red_dir = node_red_dir = os.path.realpath(node_red_dir)
            if os.path.exists(node_red_dir):
                if not { "index.js", "package.json" }.issubset(set(os.listdir(node_red_dir))):
                    raise RuntimeError("Target `node_red_dir` is not Node-RED dir format!")

                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "index.js"), os.path.join(node_red_dir, "index.js"))
            else:
                os.mkdir(node_red_dir)
                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "index.js"), os.path.join(node_red_dir, "index.js"))
                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "package.json"), os.path.join(node_red_dir, "package.json"))

        # setup Node-RED starter
        subprocess.call(
            [ self.__npm_path, "install" ],
            stdout = subprocess.DEVNULL,
            stderr = subprocess.STDOUT,
            cwd = self.node_red_dir
        )

    @property
    def editor_theme(self) -> REDTheme:
        return self.__editor_theme
    
    @property
    def node_auths(self) -> AuthCollection:
        return self.__node_auths
    
    def __save_config(self, is_ready:bool):
        with open(os.path.join(self.node_red_dir, "config.json"), "w", encoding = "utf-8") as cfw:
            json.dump({
                "userDir": self.user_dir,
                "adminRoot": self.admin_root,
                "nodeRoot": self.node_root,
                "port": self.port,
                "defaultFlow": self.default_flow,
                "enableRemoteAccess": self.remote_access,
                "showDefaultCategory": self.default_category_visible,
                "userCategory": list(set([ node.category for node in RED.registered_nodes ])),
                "editorTheme": self.editor_theme.to_dict(),
                "adminAuth": [] if is_ready else self.node_auths.to_list()
            }, cfw, indent = 4)
    
    def register(self, node_func:MethodType, name:str, category:str = "nodered_py", version:str = "1.0.0", description:str = "", author:str = "nodered.py", keywords:List[str] = [], icon:str = "function.png", properties:List[Property] = []):
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
        version: str, default 1.0.0
            version of Node
        description: str, default ""
            description of Node
        author: str, default nodered.py
            author of Node
        keywords: List[str], default []
            extra keywords of Node
        icon: str, default function.png
            icon of Node(html)
        properties: List[noderedpy._property.Property]
            propertis of Node
        """
        RED.registered_nodes.append(
            Node(
                name, category,
                version, description, author, keywords,
                icon, properties, node_func
            )
        )

    # write output
    def __write_output(self, output_file:str, res:dict):
        try:
            with open(output_file, "w", encoding = "utf-8") as ofw:
                json.dump(res, ofw, indent = 4)
        except:
            os.remove(output_file)
            res["req"]["body"] = {}
            self.__write_output(output_file, res)

    # check input and run node
    def __check_input_from_node(self):
        input_file, output_file = os.path.join(self.__cache_dir, "input.json"), os.path.join(self.__cache_dir, "output.json")

        while True:
            if os.path.exists(input_file):
                # read input file
                while True:
                    # if cannot read file or read during file writing, read file until can read
                    try:
                        with open(input_file, "r", encoding = "utf-8") as ifr:
                            input_data = json.load(ifr)
                        
                        os.remove(input_file)
                        break
                    except json.JSONDecodeError:
                        pass

                node = list(filter(lambda n: n.name == input_data["name"], RED.registered_nodes))[0]

                self.__write_output(
                    output_file,
                    node.run(input_data["props"], input_data["msg"])
                )

    def start(self, callback:MethodType = None, debug:bool = True, start_browser:bool = True):
        """
        Start Node-RED server

        Parameters
        ----------
        debug: bool, default True
            show outputs on console or not
        callback: MethodType, default None
            callback when Node-RED server started
        """

        # setup user_dir
        self.__start_for_ready()

        # set started flag file
        self.__started_file = os.path.join(self.node_red_dir, "started")
        # kill if process listen on port
        self.stop()

        # set cache_dir
        self.__cache_dir = os.path.join(self.user_dir, ".cache")
        if os.path.exists(self.__cache_dir):
            shutil.rmtree(self.__cache_dir)

        os.mkdir(self.__cache_dir)

        # save configs
        self.__save_config(False)

        # remove existing nodes
        for node_dir in glob(os.path.join(self.user_dir, "node_modules", "nodered-py-*")):
            shutil.rmtree(node_dir)

        # create custom nodes
        for node in RED.registered_nodes:
            node.create(self.user_dir, self.__cache_dir)

        # run Node-RED server
        subprocess.Popen([
            self.__node_path,
            "index.js"
        ], shell = False, stdout = sys.stdout if debug else subprocess.DEVNULL, stderr = subprocess.STDOUT, cwd = self.node_red_dir)

        while True:
            if os.path.exists(self.__started_file):
                if start_browser:
                    import webbrowser
                    webbrowser.open_new(f"http://127.0.0.1:{self.port}{self.admin_root}")

                if callback:
                    callback()

                break

        try:
            self.__check_input_from_node()
        except KeyboardInterrupt:
            self.stop()

    def __start_for_ready(self):
        """
        Start Node-RED for setup default userDir
        """
        import time

        self.__started_file = os.path.join(self.node_red_dir, "started")
        if os.path.exists(self.__started_file):
            os.remove(self.__started_file)

        # save configs
        self.__save_config(True)

        subprocess.Popen([
            self.__node_path,
            "index.js"
        ], shell = False, stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT, cwd = self.node_red_dir)

        while True:
            if os.path.exists(self.__started_file):
                self.stop()
                break

        time.sleep(1)

    def stop(self):
        """
        Stop Node-RED server
        """
        import psutil, signal

        if os.path.exists(self.__started_file):
            os.remove(self.__started_file)

        killed = False
        for process in psutil.process_iter():
            try:
                for conns in process.connections(kind = "inet"):
                    if conns.laddr.port == self.port:
                        process.send_signal(signal.SIGTERM)
                        killed = True
                        break
            except ( psutil.AccessDenied, psutil.ZombieProcess ):
                pass

            if killed:
                break

class REDBuilder:
    def __init__(self):
        self.__user_dir:str = None
        self.__node_red_dir:str = None
        self.__admin_root:str = "/node-red-py"
        self.__node_root:str = "/"
        self.__port:int = 1880
        self.__default_flow:str = "noderedpy.json"
        self.__remote_access:bool = True
        self.__default_category_visible:bool = True

    def set_user_dir(self, user_dir:str) -> "REDBuilder":
        self.__user_dir = user_dir
        return self
    
    def set_node_red_dir(self, node_red_dir:str) -> "REDBuilder":
        self.__node_red_dir = node_red_dir
        return self
    
    def set_admin_root(self, admin_root:str) -> "REDBuilder":
        self.__admin_root = admin_root
        return self
    
    def set_node_root(self, node_root:str) -> "REDBuilder":
        self.__node_root = node_root
        return self
    
    def set_port(self, port:int) -> "REDBuilder":
        self.__port = port
        return self
    
    def set_default_flow(self, flow_file:str) -> "REDBuilder":
        self.__default_flow = flow_file
        return self

    def set_remote_access(self, remote_access:bool) -> "REDBuilder":
        self.__remote_access = remote_access
        return self
    
    def set_default_category_visible(self, default_category_visible:bool) -> "REDBuilder":
        self.__default_category_visible = default_category_visible
        return self
    
    def build(self) -> RED:
        if self.__user_dir is None:
            raise ValueError("`user_dir` must be set!")

        return RED(
            self.__user_dir, self.__node_red_dir,
            self.__admin_root, self.__node_root, self.__port, self.__default_flow,
            self.__remote_access, self.__default_category_visible
        )


class NodeCommunicator:
    def __init__(self, message_file:str, node_name:str):
        self.__message_file, self.__node_name = message_file, node_name

    def log(self, *args):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "log": args
            }, mfw, indent = 4)

    def warn(self, *args):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "warn": args
            }, mfw, indent = 4)

    def error(self, *args):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "error": args
            }, mfw, indent = 4)

    def status(self, fill:Literal["red", "green", "yellow", "blue", "grey"], shape:Literal["ring", "dot"], text:str):
        with open(self.__message_file, "w", encoding = "utf-8") as mfw:
            json.dump({
                "name": self.__node_name,
                "status": { "fill": fill, "shape": shape, "text": text }
            }, mfw, indent = 4)

class Node:
    def __init__(self, name:str, category:str, version:str, description:str, author:str, keywords:List[str], icon:str, properties:List[Property], node_func:MethodType):
        # name of node cannot contain spaces
        if " " in name.strip():
            raise NameError("Node name cannot contain spaces!")
        
        # category of node cannot contain - or ,
        if "-" in category.strip() or "," in category.strip():
            raise NameError("Category cannot contain '-' or ','!")
        
        # remove default keyword in extra keywords
        self.keywords = [
            keyword
            for keyword in keywords
            if not keyword in ( "node-red", )
        ]

        self.name, self.category, self.version, self.description, self.author, self.icon, self.properties =\
            name, category, version, description, author, icon, properties
        
        self.__node_func = node_func

    def create(self, node_red_user_dir:str, node_red_user_cache_dir:str):
        self.__communicator = NodeCommunicator(os.path.join(node_red_user_cache_dir, "message.json"), self.name)
        node_dir = os.path.join(node_red_user_dir, "node_modules", self.name if self.name.startswith("nodered-py-") else f"nodered-py-{self.name}")
        os.makedirs(os.path.join(node_dir, "lib"))

        with open(os.path.join(node_dir, "package.json"), "w", encoding = "utf-8") as pjw:
            pjw.write(package_json(self))

        with open(os.path.join(node_dir, "lib", f"{self.name}.html"), "w", encoding = "utf-8") as nhw:
            nhw.write(node_html(self))

        with open(os.path.join(node_dir, "lib", f"{self.name}.js"), "w", encoding = "utf-8") as njw:
            njw.write(node_js(self, node_red_user_cache_dir))

    def run(self, props:dict, msg:dict) -> dict:
        print(f"\n{self.name} started\n===================================")
        try:
            resp = self.__node_func(self.__communicator, props, msg)
            print("============================= ended\n")

            resp.update({ "state": "success", "name": self.name })

            return resp
        except:
            return { "state": "fail", "name": self.name, "message": traceback.format_exc() }

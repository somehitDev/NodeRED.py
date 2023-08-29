# -*- coding: utf-8 -*-
import os, sys, subprocess, json, shutil
from glob import glob
from typing import List, Literal, Union
from types import MethodType
from .node import Node
from .route import Route, StaticRoute
from .theme import REDTheme
from .auth import AuthCollection
from ..__property__ import Property
from .. import __path__


class RED:
    """
    Node-RED manager class
    """
    registered_nodes:List[Node] = []
    registered_routes:List[Route] = []

    def __init__(self, user_dir:str, node_red_dir:str, admin_root:str, node_root:str, port:int, default_flow:str, remote_access:bool, default_category_visible:bool):
        """
        Set configs of Node-RED and setup

        Parameters
        ----------
        user_dir: str
            userDir of Node-RED settings
        node_red_dir: str
            directory for Node-RED starter
        admin_root: str
            httpAdminRoot of Node-RED settings
        node_root: str
            httpNodeRoot of Node-RED settings
        port: int
            port of Node-RED server
        default_flow: str
            flowFile of Node-RED settings
        remote_access: bool
            enable remote access of Node-RED or not
        default_category_visible: bool
            show default categories of Node-RED or not
        """
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

                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "route.js"), os.path.join(node_red_dir, "route.js"))
                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "index.js"), os.path.join(node_red_dir, "index.js"))
            else:
                os.mkdir(node_red_dir)
                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "route.js"), os.path.join(node_red_dir, "route.js"))
                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "index.js"), os.path.join(node_red_dir, "index.js"))
                shutil.copyfile(os.path.join(__path__[0], "node-red-starter", "package.json"), os.path.join(node_red_dir, "package.json"))

        self.__started_file = os.path.join(self.node_red_dir, "started")

        # setup Node-RED starter
        subprocess.call(
            [ self.__npm_path, "install" ],
            stdout = subprocess.DEVNULL,
            stderr = subprocess.STDOUT,
            cwd = self.node_red_dir
        )

    @property
    def editor_theme(self) -> REDTheme:
        """
        editorTheme of Node-RED server (for detail information, see https://github.com/node-red/node-red/wiki/Design:-Editor-Themes)
        """
        return self.__editor_theme
    
    @property
    def node_auths(self) -> AuthCollection:
        """
        adminAuth of Node-RED settings (for detail information, see `Editor & Admin API secutity` section of https://nodered.org/docs/user-guide/runtime/securing-node-red)
        """
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
                "adminAuth": [] if is_ready else self.node_auths.to_list(),
                "cacheDir": os.path.join(self.user_dir, ".cache"),
                "routes": [
                    route.to_dict()
                    for route in RED.registered_routes
                ]
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
            icon of Node (for detail information, see https://nodered.org/docs/creating-nodes/appearance)
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

    def route(route_func:MethodType, url:str, method:Literal["get", "post"]):
        """
        Function to register route to Node-RED

        Parameters
        ----------
        route_func: MethodType, required
            route function to register
        url: str, required
            url of route point
        method: str, required
            method of route point
            options: get, post
        """
        RED.registered_routes.append(
            Route(url, method, route_func)
        )

    def static(self, url:str, path:os.PathLike):
        """
        Function to register route to Node-RED

        Parameters
        ----------
        url: str, required
            url of static point
        path: PathLike, required
            file path for static point
        """
        RED.registered_routes.append(
            StaticRoute(url, path)
        )

    # check input(node)
    def __check_node_input(self, node_input_file:os.PathLike, node_output_file:os.PathLike):
        # if node input exists
        if os.path.exists(node_input_file):
            # read input file
            while True:
                # if cannot read file or read during file writing, read file until can read
                try:
                    with open(node_input_file, "r", encoding = "utf-8") as ifr:
                        input_data = json.load(ifr)
                    
                    os.remove(node_input_file)
                    break
                except json.JSONDecodeError:
                    pass

            node = list(filter(lambda n: n.name == input_data["name"], RED.registered_nodes))[0]

            self.__write_node_output(
                node_output_file,
                node.run(input_data["props"], input_data["msg"])
            )

    # write output(node)
    def __write_node_output(self, output_file:str, res:dict):
        try:
            with open(output_file, "w", encoding = "utf-8") as ofw:
                json.dump(res, ofw, indent = 4)
        except:
            os.remove(output_file)
            res["req"]["body"] = {}
            self.__write_node_output(output_file, res)

    # check input(route)
    def __check_route_input(self, route_input_file:os.PathLike, route_output_file:os.PathLike):
        # if route input exists
        if os.path.exists(route_input_file):
            # read input file
            while True:
                # if cannot read file or read during file writing, read file until can read
                try:
                    with open(route_input_file, "r", encoding = "utf-8") as ifr:
                        input_data = json.load(ifr)
                    
                    os.remove(route_input_file)
                    break
                except json.JSONDecodeError:
                    pass

            route:Route = list(filter(lambda r: r.url == input_data["url"], RED.registered_routes))[0]
            self.__write_route_output(
                route_output_file,
                route.run(input_data["data"])
            )

    # write output(route)
    def __write_route_output(self, output_file:str, res:Union[str, dict]):
        with open(output_file, "w", encoding = "utf-8") as ofw:
            if isinstance(res, str):
                ofw.write(res)
            else:
                json.dump(res, ofw, indent = 4)


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
        # kill if process listen on port
        self.stop()

        # set cache_dir
        self.__cache_dir = os.path.join(self.user_dir, ".cache")
        if os.path.exists(self.__cache_dir):
            shutil.rmtree(self.__cache_dir)

        os.mkdir(self.__cache_dir)

        # remove existing nodes
        for node_dir in glob(os.path.join(self.user_dir, "node_modules", "nodered-py-*")):
            shutil.rmtree(node_dir)

        # create custom nodes
        for node in RED.registered_nodes:
            node.create(self.user_dir, self.__cache_dir)

        if self.editor_theme.page.favicon is not None:
            favicon_file = os.path.join(self.node_red_dir, "favicon.ico")
            # convert png to ico if not ico file
            if not os.path.splitext(self.editor_theme.page.favicon)[-1] == ".ico":
                from PIL import Image

                Image.open(self.editor_theme.page.favicon).save(
                    favicon_file
                )
            # if ico, copy file
            else:
                shutil.copyfile(
                    self.editor_theme.page.favicon,
                    favicon_file
                )

            # self.editor_theme.page.favicon = favicon_file

        # save configs
        self.__save_config(False)

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
            while True:
                self.__check_node_input(
                    os.path.join(self.__cache_dir, "node_input.json"),
                    os.path.join(self.__cache_dir, "node_output.json")
                )
                self.__check_route_input(
                    os.path.join(self.__cache_dir, "route_input.json"),
                    os.path.join(self.__cache_dir, "route_output.json")
                )
        except KeyboardInterrupt:
            self.stop()

    def __start_for_ready(self):
        """
        Start Node-RED for setup default userDir
        """
        # stop for safety
        self.stop()

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

        import time
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

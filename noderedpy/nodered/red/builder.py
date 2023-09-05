# -*- coding: utf-8 -*-
from typing import List
from .red import RED


class REDBuilder:
    def __init__(self):
        """
        Class to create RED using Builder-Pattern
        """
        self.__user_dir:str = None
        self.__node_red_dir:str = None
        self.__admin_root:str = "/node-red-py"
        self.__node_root:str = "/"
        self.__port:int = 1880
        self.__default_flow:str = "noderedpy.json"
        self.__remote_access:bool = True
        self.__default_categories:List[str] = [ "subflows", "common", "function", "network", "sequence", "parser", "storage" ]
        self.__node_globals:dict = {}

    def set_user_dir(self, user_dir:str) -> "REDBuilder":
        """
        Function to set user_dir

        Parameters
        ----------
        user_dir: str
            userDir of Node-RED settings
        
        Return
        ------
        builder:REDBuilder
        """
        self.__user_dir = user_dir
        return self
    
    def set_node_red_dir(self, node_red_dir:str) -> "REDBuilder":
        """
        Function to set node_red_dir

        Parameters
        ----------
        node_red_dir: str
            directory for Node-RED starter
        
        Return
        ------
        builder:REDBuilder
        """
        self.__node_red_dir = node_red_dir
        return self
    
    def set_admin_root(self, admin_root:str) -> "REDBuilder":
        """
        Function to set admin_root

        Parameters
        ----------
        admin_root: str
            httpAdminRoot of Node-RED settings

        Return
        ------
        builder:REDBuilder
        """
        self.__admin_root = admin_root
        return self
    
    def set_node_root(self, node_root:str) -> "REDBuilder":
        """
        Function to set node_root

        Parameters
        ----------
        node_root: str
            httpNodeRoot of Node-RED settings
        
        Return
        ------
        builder:REDBuilder
        """
        self.__node_root = node_root
        return self
    
    def set_port(self, port:int) -> "REDBuilder":
        """
        Function to set port

        Parameters
        ----------
        port: int
            port of Node-RED server
        
        Return
        ------
        builder:REDBuilder
        """
        self.__port = port
        return self
    
    def set_default_flow(self, flow_file:str) -> "REDBuilder":
        """
        Function to set default_flow

        Parameters
        ----------
        flow_file: str
            flowFile of Node-RED settings

        Return
        ------
        builder:REDBuilder
        """
        self.__default_flow = flow_file
        return self

    def set_remote_access(self, remote_access:bool) -> "REDBuilder":
        """
        Function to set remote_access

        Parameters
        ----------
        remote_access: bool
            enable remote access of Node-RED or not
        
        Return
        ------
        builder:REDBuilder
        """
        self.__remote_access = remote_access
        return self
    
    def set_default_categories(self, default_categories:List[str]) -> "REDBuilder":
        """
        Function to set default_categories

        Parameters
        ----------
        default_categories: List[str]
            list of categories to show default
            (for detail information, see `Editor Configuration/paletteCategories` section of https://nodered.org/docs/user-guide/runtime/configuration)

        Return
        ------
        builder:REDBuilder
        """
        self.__default_categories = default_categories
        return self
    
    def set_node_globals(self, node_globals:dict) -> "REDBuilder":
        """
        Function to set node_globals

        Parameters
        ----------
        node_globals: dict
            global variables for Node-RED

        Return
        ------
        builder:REDBuilder
        """
        self.__node_globals = node_globals
        return self
    
    def build(self) -> RED:
        """
        Function to create RED from setups

        Return
        ------
        red:RED
        """

        if self.__user_dir is None:
            raise ValueError("`user_dir` must be set!")

        return RED(
            self.__user_dir, self.__node_red_dir,
            self.__admin_root, self.__node_root, self.__port, self.__default_flow,
            self.__remote_access, self.__default_categories, self.__node_globals
        )

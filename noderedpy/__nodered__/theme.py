# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass, field
from .. import __path__


@dataclass
class PageTheme:
    title:str = field(default = "Node-RED.py")
    favicon:str = field(default = os.path.join(__path__[0], "assets", "python-logo.png"))

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "favicon": self.favicon
        }

@dataclass
class HeaderTheme:
    title:str = field(default = "Node-RED.py")
    image:str = field(default = None)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "image": self.image
        }

@dataclass
class MenuTheme:
    menu_item_palette:bool = False

    def to_dict(self) -> dict:
        return {
            "menu-item-palette": self.menu_item_palette
        }

@dataclass
class PaletteTheme:
    editable:bool = True

    def to_dict(self) -> dict:
        return {
            "editable": self.editable
        }

@dataclass
class ProjectsTheme:
    enabled:bool = True

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled
        }

class REDTheme:
    def __init__(self):
        self.__page_theme, self.__header_theme, self.__menu_theme, self.__palette_theme, self.__projects_theme =\
            PageTheme(), HeaderTheme(), MenuTheme(), PaletteTheme(), ProjectsTheme()
        self.__tours, self.__user_menu = False, True

    @property
    def page(self) -> PageTheme:
        return self.__page_theme
    
    @property
    def header(self) -> HeaderTheme:
        return self.__header_theme
    
    @property
    def menu(self) -> MenuTheme:
        return self.__menu_theme
    
    @property
    def tours(self) -> bool:
        return self.__tours
    
    @tours.setter
    def tours(self, value:bool):
        self.__tours = value

    @property
    def user_menu(self) -> bool:
        return self.__user_menu
    
    @user_menu.setter
    def user_menu(self, value:bool):
        self.__user_menu = value
    
    @property
    def palette(self) -> PaletteTheme:
        return self.__palette_theme
    
    @property
    def projects(self) -> ProjectsTheme:
        return self.__projects_theme

    def to_dict(self) -> dict:
        return {
            "page": self.page.to_dict(),
            "header": self.header.to_dict(),
            "menu": self.menu.to_dict(),
            "tours": self.tours,
            "userMenu": self.user_menu,
            "palette": self.palette.to_dict(),
            "projects": self.projects.to_dict()
        }

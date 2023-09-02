# -*- coding: utf-8 -*-
"""
make python function to Node-RED node
"""

from .__nodered__.red import RED, REDBuilder
from .__nodered__.node import NodeCommunicator as Node
from .__nodered__.auth import Auth
from .__property__ import (
    PropertyDivider,
    InputProperty, ListProperty, DictProperty, CodeProperty,
    SpinnerProperty, CheckBoxProperty, ComboBoxProperty
)

__version__ = "0.2.12"
__author__ = "oyajiDev"
__email__ = "this.dev.somehit@gmail.com"

__all__ = [
    "RED", "REDBuilder", "Auth", "Node",
    "PropertyDivider", "InputProperty", "ListProperty", "DictProperty", "CodeProperty",
    "SpinnerProperty", "CheckBoxProperty", "ComboBoxProperty"
]

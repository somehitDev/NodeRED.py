# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Literal, List


@dataclass
class Auth:
    username:str
    password:str
    permissions:Literal["*", "read"] = field(default = "*")

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "permissions": self.permissions
        }

class AuthCollection:
    def __init__(self):
        self.__auths:List[Auth] = []

    def append(self, auth:Auth):
        if not auth in self.__auths:
            self.__auths.append(auth)

    def remove(self, auth:Auth):
        if auth in self.__auths:
            self.__auths.remove(auth)

    def to_list(self) -> List[dict]:
        return [
            auth.to_dict()
            for auth in self.__auths
            if auth.username is not None and auth.password is not None
        ]

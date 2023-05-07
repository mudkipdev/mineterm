from typing import Any
import json
import os


class Settings:
    def __init__(self, path: str, /) -> None:
        self.path = path
        if not os.path.exists(path):
            with open(path) as settings_file:
                self.data = json.load(settings_file)
        else:
            with open(path, "w+") as settings_file:
                self.data = {}

    def write(self) -> None:
        with open(self.path, "r+") as settings_file:
            json.dump(self.data, settings_file)


class JavaNotFoundException(Exception):
    pass

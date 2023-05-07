from __future__ import annotations

from typing import TYPE_CHECKING
from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Button, Input
from game import Version, VersionManager

if TYPE_CHECKING:
    from mineterm import MineTerm


class LaunchButton(Button):
    def __init__(self, version: Version, /) -> None:
        super().__init__("Launch", id="launch")
        self.version = version

    def on_button_pressed(self) -> None:
        self.version.launch()


class InstanceList(Static):
    def __init__(self) -> None:
        super().__init__(id="instance_list")

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search", id="search_instance_list")
        yield ListView(
            *[
                ListItem(Label(version.short_name))
                for version in VersionManager.versions
            ]
        )


class InstanceInfo(Static):
    def __init__(self, version: Version, /) -> None:
        super().__init__(id="instance_info")
        self.version = version

    def compose(self) -> ComposeResult:
        yield Label(f"A short description about {self.version.name}...")
        yield LaunchButton(self.version)


class MineTermApp(App):
    CSS_PATH = "css/mineterm.css"

    def __init__(self, mineterm: MineTerm) -> None:
        super().__init__()
        self.mineterm = mineterm

    def compose(self) -> ComposeResult:
        yield InstanceList()
        yield InstanceInfo(VersionManager.versions[0])

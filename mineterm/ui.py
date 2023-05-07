from __future__ import annotations

from typing import TYPE_CHECKING
from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Button, Input
from textual.containers import Horizontal, Vertical
from game import Version, VersionManager

if TYPE_CHECKING:
    from mineterm import MineTerm


class LaunchButton(Button):
    def __init__(
        self,
        mineterm: MineTerm,
        version: Version,
    ) -> None:
        super().__init__("Launch", id="launch")
        self.mineterm = mineterm
        self.version = version

    def on_button_pressed(self) -> None:
        self.version.launch()
        self.mineterm.is_game_launched = True


class SearchInstanceList(Input):
    def __init__(self, mineterm: MineTerm, /) -> None:
        super().__init__(placeholder="Search", id="search_instance_list")
        self.mineterm = mineterm

    def on_input_changed(self, message: Input.Changed) -> None:
        self.mineterm.app.search(message.value)


class InstanceListView(ListView):
    def __init__(self, mineterm: MineTerm, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mineterm = mineterm

    def on_list_view_selected(self, message: ListView.Selected):
        self.version = VersionManager.get_version_from_short_name(message.item.name)


class InstanceInfo(Static):
    def __init__(self, mineterm: MineTerm, version: Version) -> None:
        super().__init__(id="instance_info")
        self.mineterm = mineterm
        self.version = version

    def compose(self) -> ComposeResult:
        yield Label(self.version.name)
        yield LaunchButton(self.mineterm, self.version)


class MineTermApp(App):
    CSS_PATH = "css/mineterm.css"

    def __init__(self, mineterm: MineTerm) -> None:
        super().__init__()
        self.mineterm = mineterm

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="instances"):
                yield SearchInstanceList(self.mineterm)
                yield InstanceListView(
                    *[
                        ListItem(
                            Label(version.short_name), classes="instance_list"
                        )
                        for version in VersionManager.versions
                    ],
                    id="instance_list",
                )

            yield InstanceInfo(
                self.mineterm, VersionManager.versions[0]
            )

    def search(self, text: str, /) -> None:
        # If you have better understanding of Textual, please PR
        # to clean up this method.
        list_view = self.query_one("#instance_list")
        children = [
            ListItem(Label(version.short_name), classes="instance")
            for version in VersionManager.versions
            if not text
            or text.lower() in version.name.lower()
            or text.lower() in version.short_name.lower()
        ]

        list_view.clear()
        for child in children:
            list_view.append(child)

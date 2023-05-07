from ui import MineTermApp
from game import VersionManager


class MineTerm:
    def __init__(self) -> None:
        self.app = MineTermApp(self)

    def main(self) -> None:
        self.app.run()

import os
from ui import MineTermApp
from game import VersionManager
from utils import Settings


class MineTerm:
    def __init__(self) -> None:
        if not os.path.exists("data"):
            os.mkdir("data")

        self.app = MineTermApp(self)
        self.settings = Settings("data/settings.json")
        self.settings.write()

        self.is_game_launched = False

    def main(self) -> None:
        if not os.getenv("JAVA_HOME"):
            raise JavaNotFoundException(
                "Please make sure your JAVA_HOME environment variable is set."
            )

        self.app.run()

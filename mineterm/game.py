import os
import sys
import json
import subprocess

__all__ = ("Version", "VersionManager")

VERSIONS_PATH = "./resources/versions/"
# For now, this requires you to have Java on PATH:
LAUNCH_COMMAND = """\
java -Djava.library.path="{natives}" -cp "{classpath}" {entry_point}
"""

if sys.platform == "win32":
    platform = "windows"
elif sys.platform == "darwin":
    platform = "mac"
else:
    platform = "linux"


class Version:
    def __init__(self, data: dict, /) -> None:
        self.name = data["name"]
        self.short_name = data.get("short_name", data["name"])
        self.entry_point = data["entry_point"]
        self.jvm_arguments = data.get("jvm_arguments", "")
        self.classpath = data["classpath"]
        self.natives = data["natives"]

    @property
    def launch_command(self) -> str:
        return LAUNCH_COMMAND.format(
            natives=self.natives[platform]
            classpath=(";" if platform == "windows" else ":").join(self.classpath),
            entry_point=self.entry_point,
        )

    def launch(self) -> None:
        print(self.launch_command)
        process = subprocess.Popen(
            self.launch_command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


class VersionManager:
    versions = []

    @staticmethod
    def load_versions(path: str, /) -> None:
        for version_directory in os.listdir(path):
            try:
                with open(path + version_directory + "/version.json") as version_file:
                    VersionManager.versions.append(Version(json.load(version_file)))
            except FileNotFoundError as exception:
                print(f'Tried to load invalid version "{version_directory}"')


VersionManager.load_versions(VERSIONS_PATH)

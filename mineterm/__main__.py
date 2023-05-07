import os
from mineterm import MineTerm


def main() -> None:
    if not os.getenv("JAVA_HOME"):
        raise JavaNotFoundException(
            "Please make sure your JAVA_HOME environment variable is set."
        )

    mineterm = MineTerm()
    mineterm.main()


if __name__ == "__main__":
    main()

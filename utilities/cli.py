import shlex
import subprocess
from enum import Enum
from typing import Iterable


class ColorAffix(str, Enum):
    RESET = "\x1b[0m"
    BRIGHT = "\x1b[1m"
    DIM = "\x1b[2m"
    UNDERSCORE = "\x1b[4m"
    BLINK = "\x1b[5m"
    REVERSE = "\x1b[7m"
    HIDDEN = "\x1b[8m"
    FG_BLACK = "\x1b[30m"
    FG_RED = "\x1b[31m"
    FG_GREEN = "\x1b[32m"
    FG_YELLOW = "\x1b[33m"
    FG_BLUE = "\x1b[34m"
    FG_MAGENTA = "\x1b[35m"
    FG_CYAN = "\x1b[36m"
    FG_WHITE = "\x1b[37m"
    BG_BLACK = "\x1b[40m"
    BG_RED = "\x1b[41m"
    BG_GREEN = "\x1b[42m"
    BG_YELLOW = "\x1b[43m"
    BG_BLUE = "\x1b[44m"
    BG_MAGENTA = "\x1b[45m"
    BG_CYAN = "\x1b[46m"
    BG_WHITE = "\x1b[47m"


def color_text(text: str, colors: Iterable[ColorAffix]) -> str:
    prefixes = "".join(color for color in colors)
    suffixes = ColorAffix.RESET
    return prefixes + text + suffixes


def parse_command(cmd: str) -> list[str]:
    return shlex.split(cmd)


def run(cmd: str, hide_output=True):
    """
    https://stackoverflow.com/q/11269575

    ```
    run('echo "Hello, world!"')
    ```
    """

    if hide_output:
        subprocess.run(
            parse_command(cmd),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        return

    subprocess.run(parse_command(cmd))

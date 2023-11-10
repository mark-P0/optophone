import textwrap as tw
from enum import IntEnum
from typing import Literal

from ...utilities import cli


class Levels:
    """
    Can be arbitrary values as well

    https://android.googlesource.com/platform/external/svox/+/refs/heads/master/pico/tts/svox_ssml_parser.cpp#24
    """

    class Pitch(IntEnum):
        XLOW = 50
        LOW = 75
        MEDIUM = 100
        HIGH = 150
        XHIGH = 200

    class Rate(IntEnum):  # Speaking speed
        XSLOW = 30
        SLOW = 60
        MEDIUM = 100
        FAST = 250
        XFAST = 500

    class Volume(IntEnum):
        SILENT = 0
        XLOW = 25
        LOW = 70
        MEDIUM = 120
        LOUD = 300
        XLOUD = 450


def format(
    text: str,
    pitch: Levels.Pitch = Levels.Pitch.MEDIUM,
    rate: Levels.Rate = Levels.Rate.SLOW,
    volume: Levels.Volume = Levels.Volume.LOW,
):
    """
    Speech synthesis can be tweaked by wrapping source text in specific "tags"

    https://android.googlesource.com/platform/external/svox/+/refs/heads/master/pico/tts/com_svox_picottsengine.cpp#67
    """

    text = f"<pitch  level='{pitch}' >{text}</pitch >"
    text = f"<speed  level='{rate}'  >{text}</speed >"
    text = f"<volume level='{volume}'>{text}</volume>"
    return text


def generate_wav(
    text: str,
    language: Literal["en-US", "en-GB", "de-DE", "es-ES", "fr-FR", "it-IT"],
    filename="tts.wav",
) -> str:
    filepath = f"/tmp/{filename}"
    cli.run(
        tw.dedent(
            f"""
            pico2wave
            --wave={filepath}
            --lang={language}
            "{format(text)}"
            """
        )
        .strip()
        .replace("\n", " ")
    )
    return filepath

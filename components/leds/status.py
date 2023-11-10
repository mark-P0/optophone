from typing import Literal

from gpiozero import RGBLED
from loguru import logger

from ...utilities import events
from ...utilities.cli import ColorAffix, color_text

led = RGBLED(
    red=16,
    green=20,
    blue=21,
    initial_value=(0, 0, 0),
)

output: Literal["braille", "tts", None] = "tts"


@events.SHUTDOWN.subscribe
async def on_shutdown(*_):
    global output
    output = None

    led.value = (0, 0, 0)
    text = color_text(
        "None",
        (
            ColorAffix.FG_BLACK,
            ColorAffix.BG_WHITE,
        ),
    )
    logger.debug(f"Status LED: {text}")


@events.WAITING_FOR_DOCUMENT.subscribe
async def on_waiting_for_document(*_):
    global output
    output = None

    led.value = (1, 0, 0)
    text = color_text(
        "Red",
        (
            ColorAffix.FG_RED,
            ColorAffix.BG_BLACK,
        ),
    )
    logger.debug(f"Status LED: {text}")


@events.DOCUMENT_FOUND.subscribe
async def on_document_found(*_):
    led.value = (1, 0.25, 0)
    text = color_text(
        "Yellow",
        (
            ColorAffix.FG_YELLOW,
            ColorAffix.BG_BLACK,
        ),
    )
    logger.debug(f"Status LED: {text}")


@events.OUTPUT_BRAILLE.subscribe
async def on_output_braille(*_):
    global output
    output = "braille"


@events.OUTPUT_TTS.subscribe
async def on_output_tts(*_):
    global output
    output = "tts"


@events.OUTPUT_DISPLAY.subscribe
async def on_output_display(*_):
    global output

    if output == "braille":
        led.value = (0, 1, 0)
        text = color_text(
            "Green",
            (
                ColorAffix.FG_GREEN,
                ColorAffix.BG_BLACK,
            ),
        )
        logger.debug(f"Status LED: {text}")

    if output == "tts":
        led.value = (0, 0, 1)
        text = color_text(
            "Blue",
            (
                ColorAffix.FG_BLUE,
                ColorAffix.BG_BLACK,
            ),
        )
        logger.debug(f"Status LED: {text}")


if __name__ == "__main__":
    breakpoint()

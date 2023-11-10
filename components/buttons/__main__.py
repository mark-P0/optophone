# flake8: noqa: F401 - Imported modules have event listeners that must be "executed" (via the act of importing)

from loguru import logger

from ...utilities import events
from . import power, toggle
from .white import left as white_left
from .white import right as white_right
from .yellow import left as yellow_left
from .yellow import right as yellow_right


@events.OUTPUT_TOGGLE.subscribe
async def on_output_toggle(*_):
    logger.info("Toggle button triggered")


@events.BUTTON_YELLOW_LEFT.subscribe
async def on_left_yellow_button(*_):
    logger.info("Yellow left triggered")


@events.BUTTON_YELLOW_RIGHT.subscribe
async def on_right_yellow_button(*_):
    logger.info("Yellow right triggered")


@events.BUTTON_WHITE_LEFT.subscribe
async def on_left_white_button(*_):
    logger.info("White left triggered")


@events.BUTTON_WHITE_RIGHT.subscribe
async def on_right_white_button(*_):
    logger.info("White right triggered")


events.loop.run_forever()

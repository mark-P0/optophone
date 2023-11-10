# flake8: noqa: E402 - Imports are interleaved with log statements so they are not all at the top
# flake8: noqa: F401 - Imported modules are not necessarily used here, but have event listeners that must be "executed" (via the act of importing) in this entrypoint file for them to work.

from loguru import logger

logger.add("/tmp/{time}.log")

logger.info("Importing buttons & LEDs...")
from .components.buttons import power as power_button
from .components.buttons import toggle
from .components.buttons.white import left as white_left
from .components.buttons.white import right as white_right
from .components.buttons.yellow import left as yellow_left
from .components.buttons.yellow import right as yellow_right
from .components.leds import power as power_led
from .components.leds import status, strip

logger.info("Importing major components...")
from .components import camera, prox, registers, speakers
from .utilities import events

logger.info("Imports finished.")


events.POWERUP.publish(None)
events.loop.run_forever()

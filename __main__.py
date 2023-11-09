from loguru import logger

logger.add("/tmp/{time}.log")
logger.info("Importing buttons & LEDs...")

from .components.buttons import (
    power as power_button,
)
from .components.buttons import toggle
from .components.buttons.white import (
    left as white_left,
)
from .components.buttons.white import (
    right as white_right,
)
from .components.buttons.yellow import (
    left as yellow_left,
)
from .components.buttons.yellow import (
    right as yellow_right,
)
from .components.leds import (
    power as power_led,
)
from .components.leds import status, strip

logger.info(
    "Importing major components..."
)

from .components import (
    camera,
    prox,
    registers,
    speakers,
)
from .utilities import events

logger.info("Imports finished.")


events.POWERUP.publish(None)
events.loop.run_forever()

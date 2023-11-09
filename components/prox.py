"""
https://learn.adafruit.com/scanning-i2c-addresses/raspberry-pi
https://learn.adafruit.com/adafruit-apds9960-breakout/circuitpython
"""

import time

import board
from adafruit_apds9960.apds9960 import (
    APDS9960,
)
from loguru import logger

from ..utilities import asynch, events
from ..utilities.file_inputs import (
    Maintained,
)
from .leds import strip


def initialize_prox():
    global prox

    while ...:
        try:
            prox = APDS9960(board.I2C())
            prox.enable_proximity = True
            logger.debug(
                "Initialized prox"
            )
            return prox
        except:
            logger.debug(
                "Failed to initialize prox; retrying..."
            )
            pass


fileprox = Maintained(
    "/home/squid/Documents/optophone/components/prox.py"
)
prox = initialize_prox()

GRACE_PERIOD = 5

ASSERTION_THRESHOLD = 3
assert_ct = 0
is_asserted = False
is_active = True


@events.POWERUP.subscribe
async def on_powerup(*_):
    logger.info("Waiting for document...")
    events.WAITING_FOR_DOCUMENT.publish(
        None
    )


@events.OUTPUT_BRAILLE.subscribe
async def on_output_braille(*_):
    global is_active
    is_active = True  # Reactivate prox only on output stage


@events.OUTPUT_TTS.subscribe
async def on_output_tts(*_):
    global is_active
    is_active = True  # Reactivate prox only on output stage


def has_something_in_proximity():
    global fileprox, prox

    return fileprox.state or (
        100 < prox.proximity
    )


@asynch.periodic(0.1)
def poll():
    global ASSERTION_THRESHOLD, assert_ct, is_asserted, is_active, prox
    try:
        # print(prox.proximity)
        # return

        if not is_active:
            return

        if not (
            (
                has_something_in_proximity()
                and (not is_asserted)
            )
            or (
                (
                    not has_something_in_proximity()
                )
                and is_asserted
            )
        ):
            return

        if (
            assert_ct
            < ASSERTION_THRESHOLD
        ):
            assert_ct += 1
            return

        is_asserted = not is_asserted
        assert_ct = 0

        if is_asserted:
            strip.on()
            logger.debug(
                "Grace period start..."
            )
            time.sleep(GRACE_PERIOD)
            logger.debug(
                "Grace period end."
            )

            if (
                not has_something_in_proximity()
            ):
                logger.debug(
                    "Proximity lost after grace period"
                )
                strip.off()
                return

            logger.info("Document found.")
            events.DOCUMENT_FOUND.publish(
                None
            )
            is_active = False  # Deactivate prox when paper was found
        else:
            logger.info("Document lost.")
            strip.off()
            events.WAITING_FOR_DOCUMENT.publish(
                None
            )
    except:
        logger.debug("Prox crashed(?)")
        prox = initialize_prox()


if __name__ == "__main__":

    @events.DOCUMENT_FOUND.subscribe
    async def on_document_found(*_):
        global is_active
        is_active = True

    events.loop.run_forever()

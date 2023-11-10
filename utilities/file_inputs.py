"""
Used for allowing source files to be a source of input,
e.g. for testing without actually interacting with hardware

https://learn.sparkfun.com/tutorials/button-and-switch-basics/
"""

import os
from typing import Callable

from loguru import logger

from . import asynch


class Momentary:
    """
    e.g. push buttons
    """

    def __init__(self, filename: str):
        logger.warning(f"Input to `{filename}` enabled")

        self.path = filename
        self.data = os.stat(self.path)
        self.when_pressed: Callable = lambda: ...

        @asynch.periodic()
        def poll():
            if self.is_updated:
                self.when_pressed()

    @property
    def is_updated(self):
        current_data = os.stat(self.path)
        status = self.data != current_data
        if status is True:
            self.data = current_data
        return status


class Maintained:
    """
    e.g. switches, latches, levers
    """

    def __init__(self, filename: str):
        logger.warning(f"Input to `{filename}` enabled")

        self.path = filename
        self.data = os.stat(self.path)
        self.state = False

        @asynch.periodic()
        def poll():
            if self.is_updated:
                self.state = not self.state

    @property
    def is_updated(self):
        current_data = os.stat(self.path)
        status = self.data != current_data
        if status is True:
            self.data = current_data
        return status


if __name__ == "__main__":

    def shutdown():
        print("shutdown triggered")
        asynch.loop.stop()

    power = Momentary("./utilities/file_inputs/button_power")
    power.when_pressed = shutdown

    # prox = Maintained("./utilities/file_inputs/prox")
    # while True:
    #     if prox.is_updated:
    #         print("file was updated")

    asynch.loop.run_forever()

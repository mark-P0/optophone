import asyncio
from typing import Any, Callable, Coroutine

from loguru import logger

loop = asyncio.get_event_loop()


class Event:
    def __init__(self) -> None:
        self.subscribers = []

    def subscribe(
        self, fn: Callable[[Any], Coroutine]
    ):
        self.subscribers.append(fn)

    def publish(self, data):
        """
        - Events are generally published
          from GPIO device callbacks
        - `gpiozero` runs callbacks from
          another thread
        - Tasks cannot be run on event loops
          from other threads
        ---
        - https://docs.python.org/3/library/
          asyncio-task.html
            #creating-tasks
            #asyncio.Task
            #scheduling-from-other-threads
        """
        for fn in self.subscribers:
            # loop.create_task(fn(data))  # Not thread-safe
            asyncio.run_coroutine_threadsafe(
                fn(data), loop
            )


SHUTDOWN = Event()
POWERUP = Event()
WAITING_FOR_DOCUMENT = Event()
DOCUMENT_FOUND = Event()
IMAGE_CAPTURED = Event()
OUTPUT_TTS = Event()
OUTPUT_BRAILLE = Event()
OUTPUT_DISPLAY = Event()
OUTPUT_TOGGLE = Event()
BUTTON_YELLOW_LEFT = Event()
BUTTON_YELLOW_RIGHT = Event()
BUTTON_WHITE_LEFT = Event()
BUTTON_WHITE_RIGHT = Event()

import asyncio
from typing import Callable

from . import events

should_stop_periodic = False


@events.SHUTDOWN.subscribe
async def on_shutdown(*_):
    global should_stop_periodic
    should_stop_periodic = True


def periodic(delay=0.250):
    """
    Background periodic task
    i.e. naive JS `setInterval()`
    """

    def decorator(fn: Callable):
        async def coroutine():
            while not should_stop_periodic:
                fn()
                await asyncio.sleep(delay)

        events.loop.create_task(coroutine())

    return decorator


async def sleep(seconds: float):
    await asyncio.sleep(seconds)

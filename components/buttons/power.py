from gpiozero import Button
from loguru import logger

from ...utilities import asynch, events
from ...utilities.file_inputs import Momentary

is_active = True


@events.DOCUMENT_FOUND.subscribe
async def on_document_found(*_):
    global is_active
    is_active = False
    logger.debug("Shutdown disabled")


@events.OUTPUT_DISPLAY.subscribe
async def on_output_display(*_):
    global is_active
    is_active = True
    logger.debug("Shutdown enabled")


@events.SHUTDOWN.subscribe
async def on_shutdown(*_):
    logger.info("Shutdown triggered")

    await asynch.sleep(1)  # Wait for a sec before stopping the event loop
    events.loop.stop()  # This should end the program...


def publish_shutdown_event():
    global is_active

    if not is_active:
        return

    events.SHUTDOWN.publish(None)
    logger.warning("Shutdown published")


power_file = Momentary("/home/squid/Documents/optophone/components/buttons/power.py")
power_file.when_pressed = publish_shutdown_event

power_button = Button(4, hold_time=0.5)
power_button.when_held = publish_shutdown_event


if __name__ == "__main__":
    events.loop.run_forever()

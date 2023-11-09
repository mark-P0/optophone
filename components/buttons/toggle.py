from gpiozero import Button

from ...utilities import events
from ...utilities.file_inputs import (
    Momentary,
)


def publish_toggle_event():
    events.OUTPUT_TOGGLE.publish(None)


toggle_file = Momentary(
    "/home/squid/Documents/optophone/components/buttons/toggle.py"
)
toggle_file.when_pressed = (
    publish_toggle_event
)

toggle_button = Button(5, hold_time=0.1)
toggle_button.when_held = (
    publish_toggle_event
)

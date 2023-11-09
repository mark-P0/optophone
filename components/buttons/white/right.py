from gpiozero import Button

from ....utilities import asynch, events
from ....utilities.file_inputs import (
    Momentary,
)


def publish_button_event():
    events.BUTTON_WHITE_RIGHT.publish(None)


white_right_file = Momentary(
    "/home/squid/Documents/optophone/components/buttons/white/right.py"
)
white_right_file.when_pressed = (
    publish_button_event
)

white_right_button = Button(
    26, hold_time=0.1
)
white_right_button.when_held = (
    publish_button_event
)

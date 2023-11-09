from gpiozero import Button

from ....utilities import asynch, events
from ....utilities.file_inputs import (
    Momentary,
)


def publish_button_event():
    events.BUTTON_YELLOW_RIGHT.publish(None)


yellow_right_file = Momentary(
    "/home/squid/Documents/optophone/components/buttons/yellow/right.py"
)
yellow_right_file.when_pressed = (
    publish_button_event
)

yellow_right_button = Button(
    13, hold_time=0.1
)
yellow_right_button.when_held = (
    publish_button_event
)

# flake8: noqa: F401 - Imported modules have event listeners that must be "executed" (via the act of importing)

from gpiozero import Button

from ....utilities import asynch, events
from ....utilities.file_inputs import Momentary


def publish_button_event():
    events.BUTTON_WHITE_LEFT.publish(None)


white_left_file = Momentary(
    "/home/squid/Documents/optophone/components/buttons/white/left.py"
)
white_left_file.when_pressed = publish_button_event

white_left_button = Button(19, hold_time=0.1)
white_left_button.when_held = publish_button_event

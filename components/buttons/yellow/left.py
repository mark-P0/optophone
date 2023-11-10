# flake8: noqa: F401 - Imported modules have event listeners that must be "executed" (via the act of importing)

from gpiozero import Button

from ....utilities import asynch, events
from ....utilities.file_inputs import Momentary


def publish_button_event():
    events.BUTTON_YELLOW_LEFT.publish(None)


yellow_left_file = Momentary(
    "/home/squid/Documents/optophone/components/buttons/yellow/left.py"
)
yellow_left_file.when_pressed = publish_button_event

yellow_left_button = Button(6, hold_time=0.1)
yellow_left_button.when_held = publish_button_event

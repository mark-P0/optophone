#!/bin/bash -e

# `loguru` formatting can be controlled via an environment variable
# https://loguru.readthedocs.io/en/stable/api/logger.html

# Tesseract thread limiting seems to improve performance on x64 Linux (Zorin)
# Does not seem to change anything here though...
# https://github.com/tesseract-ocr/tesseract/issues/898

# Power LED also acts as Activity LED (ACTLED)
# It is tied to GPIO 14 via /boot/config.txt
# For it to work properly, it must be released from its ACTLED triggers
# during the program, and rebound after.
# https://gpiozero.readthedocs.io/en/stable/recipes_advanced.html#controlling-the-pi-s-own-leds
#
# Power LED driven via this script rather than in Python
# `gpiozero` seems to disable the pin entirely upon exit
# https://embeddedcomputing.com/technology/processing/interface-io/quick-start-raspberry-pi-gpio-terminal-interface
# https://github.com/RPi-Distro/raspi-gpio

echo "Starting audio services (pulseaudio) (should fail if unnecessary)"
pulseaudio -D || true

echo Releasing ACTLED triggers...
echo none | sudo tee /sys/class/leds/led0/trigger > /dev/null

echo Driving ACTLED HIGH...
raspi-gpio set 14 op  # Set as output
raspi-gpio set 14 dh  # Drive high

echo Running program...
# OMP_THREAD_LIMIT=1 \
GPIOZERO_PIN_FACTORY=pigpio \
LOGURU_FORMAT="<green>{time:HH:mm:ss.SSS}</green> │ <level>{level: <6.6}</level> │ <cyan>{name: <36.36}</cyan> <cyan>{function: <12.12}</cyan> <cyan>{line: <3}</cyan> <level>{message}</level>" \
PYTHONPATH=/home/squid/Documents \
python -m $1
# python -B -m $1
# python3.9 -B -m $1
# python3 -B -m $1

echo Rebinding ACTLED triggers...
echo mmc0 | sudo tee /sys/class/leds/led0/trigger > /dev/null  # ACTLED rebind

# This relies on the above Python script exiting gracefully...
echo Execute \`sudo poweroff\`. . .
sudo poweroff

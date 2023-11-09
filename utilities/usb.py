r"""
https://raspberrypi.stackexchange.com/a/74906
https://github.com/mvp/uhubctl#raspberry-pi-3b
https://github.com/mvp/uhubctl#linux-usb-permissions
https://github.com/mvp/uhubctl/tree/d98e6deb6ed752811fd959414366ec889ac8aeec#linux-usb-permissions

sudo \     # Can be configured as not root
uhubctl \
-l 1-1 \   # RPi3B+ USB hub is named `1-1`
-p 2 \     # Hub port 2 controls power (all)
-a 0 \     #   0 |  1 |     2 |      3
           # off | on | cycle | toggle
"""

import textwrap as tw

from . import cli


def on():
    cmd = (
        tw.dedent(
            """
            uhubctl
            --location 1-1
            --ports 2
            --action on
            """
        )
        .strip()
        .replace("\n", " ")
    )
    cli.run(cmd)


def off():
    cmd = (
        tw.dedent(
            """
            uhubctl
            --location 1-1
            --ports 2
            --action off
            """
        )
        .strip()
        .replace("\n", " ")
    )
    cli.run(cmd)

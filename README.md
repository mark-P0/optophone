# Optophone

Software for an undergraduate design project for the degree of BS in Computer Engineering, ~2022.

<!--

Add project outline here...

-->

## TODO

https://raspberrypi-guide.github.io/electronics/power-consumption-tricks

## Pinout reference

https://pinout.xyz/

![](https://raw.githubusercontent.com/Gadgetoid/Pinout.xyz/master/resources/raspberry-pi-pinout.png)

https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

<!-- ![](https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg) -->

## Python GPIO libraries

https://raspberrypi.stackexchange.com/questions/58820/compare-and-contrast-python-gpio-apis

- `gpiozero` has simplest API, most modern, and has underlying support for other major libraries
  - Endorsed by Raspberry Pi Foundation itself
  - (?) Created by members of the foundation
    - Who also created https://piwheels.org/
  - https://www.raspberrypi.com/news/gpio-zero-a-friendly-python-api-for-physical-computing/
  - https://www.raspberrypi.com/documentation/computers/os.html#gpio-in-python
- `pigpio` is most detailed, most accurate (hardware-timed)
  - Endorsed by `gpiozero` docs
- `wiringPi` is closest to Arduino
  - Also rather complex
  - Issue with the author...
- `RPi.GPIO` has been the de-facto standard for a _long_ time
- `RPIO` is an extension of `RPi.GPIO`

## Test GPIO health / status

https://abyz.me.uk/rpi/pigpio/faq.html#Have_I_fried_my_GPIO

```sh
gpiotest
```

- Needs `sudo pigpiod` (`pigpio` daemon)
- This is run automatically via `~/.profile`
  - File contains caveats for when it is executed

## Execute project

As a module

- Implicitly uses top-level `__main__.py`
- `PYTHONPATH` is a Python-exclusive extension of `PATH`
- Add project directory parent to `PATH` so that it is visible
- Project directory cannot be given directly to `python`

```sh
PYTHONPATH=$(cd .. && pwd) python -m optophone
```

Use `-B` flag to avoid `__pycache__`

- https://github.com/pytest-dev/pytest/issues/200
- https://docs.python.org/3/using/cmdline.html#cmdoption-B

```sh
PYTHONPATH=$(cd .. && pwd) python -B -m optophone
```

Change `gpiozero` default pin factory

- https://gpiozero.readthedocs.io/en/stable/api_pins.html#changing-pin-factory

```sh
GPIOZERO_PIN_FACTORY=pigpio PYTHONPATH=$(cd .. && pwd) python -B -m optophone
```

Override `loguru` default formatting

- Slightly modifies default format as per docs
- https://github.com/Delgan/loguru/blob/master/loguru/_defaults.py#L31
- Aligns names

```sh
LOGURU_FORMAT="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> │ <level>{level: <8}</level> │ <cyan>{name: <32.32}</cyan> : <cyan>{function: <16.16}</cyan> : <cyan>{line: >3}</cyan> - <level>{message}</level>" \
GPIOZERO_PIN_FACTORY=pigpio \
PYTHONPATH=$(cd .. && pwd) \
python -B -m optophone
```

## Shell script

- Wrapper for above verbose one-line command
- Receives **module name** as argument

Running this...

```
./run.sh optophone
```

...is equivalent to this.

```sh
...  # Temporary environment variables
python -b -m optophone
```

## TTS commands

...

## Concepts

- Decorators
- Async
- Pubsub
- Main blocks
- Modules | Scripts | ~~Packages~~
- Files as singletons

## `uhubctl` USB permissions

- https://github.com/mvp/uhubctl#linux-usb-permissions
- https://github.com/mvp/uhubctl/tree/d98e6deb6ed752811fd959414366ec889ac8aeec#linux-usb-permissions
  - Outdated version installed (`v2.3.0-1`)

### File for rules

`/etc/udev/rules.d/52-usb.rules`

```sh
sudo nano /etc/udev/rules.d/52-usb.rules
cat /etc/udev/rules.d/52-usb.rules
```

### Rules

- One rule per hub
- 3B+ has two (2) hubs, each identified by a Vendor ID

```sh
SUBSYSTEM=="usb", ATTR{idVendor}=="0424", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", MODE="0666"
```

- Simplified rule for ALL hubs

```sh
SUBSYSTEM=="usb", MODE="0666"
```

## Hotspot | Access Point

- [RaspAP](https://raspap.com/)
- [Also via official documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#set-up-the-network-router)

### Credentials

- SSID
  - squid
  - mark1234
- Dashboard
  - squid
  - mark1234
- SSH
  - squid
  - mark1234

### Toggling

https://docs.raspap.com/faq/#can-i-turn-the-hotspot-onoff-over-ssh

- Turn on

  - Via terminal

    ```sh
    sudo systemctl start hostapd.service

    # Or...
    sudo systemctl enable hostapd dnsmasq raspapd
    sudo nano /etc/dhcpcd.conf
    ## Uncomment static IP configurations by RaspAP
    sudo reboot
    ```

- Turn off
  - Via terminal
    ```sh
    sudo systemctl stop hostapd.service
    # Or...
    sudo systemctl disable hostapd dnsmasq raspapd
    sudo nano /etc/dhcpcd.conf
    ## Comment static IP configurations by RaspAP
    sudo reboot
    ```
  - Via dashboard
    - Login to dashboard
    - Select **Hotspot** tab
    - Click **Stop Hotspot**

## SSH

`ssh squid@raspberrypi.local`

- Must connect to same network as Pi
- Pi can host required network (hotspot )

### Auto login

- Generate client key
  ```sh
  ssh-keygen -t ed25519
  ```
- Append client `~/.ssh/id_ed25519.pub` contents to host `~/.ssh/authorized_keys`
  - Can be automated by `ssh-copy-id` program

## Hostnames

### `raspberrypi.local`

- Only available for devices that support mDNS
  - https://www.raspberrypi.com/documentation/computers/remote-access.html#resolving-raspberrypi-local-with-mdns
  - Not available in Android?
    - https://blog.esper.io/android-dessert-bites-26-mdns-local-47912385/

### `10.3.141.1`

- RaspAP default IP

## VSCode

- https://code.visualstudio.com/docs/remote/remote-overview
- https://code.visualstudio.com/docs/remote/ssh

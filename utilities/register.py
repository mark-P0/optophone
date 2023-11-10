from typing import Literal

from gpiozero import DigitalOutputDevice

from . import events

OUTPUT_ENABLE = DigitalOutputDevice(12, active_high=False)
OUTPUT_ENABLE.off()


@events.SHUTDOWN.subscribe
async def on_shutdown(*_):
    OUTPUT_ENABLE.off()


class ShiftRegister:
    def __init__(self, data: int, latch: int, clock: int):
        self.pins = (
            DigitalOutputDevice(data),
            DigitalOutputDevice(latch),
            DigitalOutputDevice(clock),
        )

        self.__has_value_changed = False
        self.is_active = False
        self.value = 0

    def __set(self, pin: DigitalOutputDevice, value: Literal[0, 1]):
        clock = self.pins[2]

        clock.value = 0
        pin.value = value
        clock.value = 1

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: int):
        self.__value = new_value
        self.__has_value_changed = True

        # OUTPUT_ENABLE.off()
        self.shift_out(new_value)
        OUTPUT_ENABLE.on()
        self.shift_out(new_value)

    def shift_out(self, value: int, size=8, msb_first=True):
        """
        Sets the binary equivalent of `value` as the shift register output.
        - Default size to be taken from `value` is a byte (8 bits)
        - Default behavior is MSB-first; otherwise it will be last

        MSB-first behavior can also be implemented mathematically like so
        (Essentially an alternative reverse iteration of indices):
        ```py
        for idx in range(size):
            if msb_first: idx = size - idx - 1
            clk.value = False
            dat.value = (value >> idx) & 1
            clk.value = True
        ```
        """

        data, latch, _ = self.pins

        self.__set(latch, 0)

        rng = range(size)
        if msb_first:
            rng = reversed(rng)
        for idx in rng:
            bit = (value >> idx) & 1
            self.__set(data, bit)

        self.__set(latch, 1)

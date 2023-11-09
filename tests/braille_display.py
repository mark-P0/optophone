import time

from ..utilities import braille
from ..utilities.register import OUTPUT_ENABLE, ShiftRegister

left = ShiftRegister(17, 27, 22)
mid = ShiftRegister(10, 9, 11)
right = ShiftRegister(25, 8, 7)
left.shift_out(0)
mid.shift_out(0)
right.shift_out(0)

time.sleep(3)
for key, bits in [*braille.letters.items()][1:8]:
    print(f'{key=} {bin(bits)=}')

    left.shift_out(~bits)
    mid.shift_out(~bits)
    right.shift_out(~bits)
    OUTPUT_ENABLE.off()
    OUTPUT_ENABLE.on()
    left.shift_out(~bits)
    mid.shift_out(~bits)
    right.shift_out(~bits)

    time.sleep(2)

mid.value = 0
OUTPUT_ENABLE.off()
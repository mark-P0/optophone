import time

from ..utilities.register import OUTPUT_ENABLE, ShiftRegister

left = ShiftRegister(17, 27, 22)
mid = ShiftRegister(10, 9, 11)
right = ShiftRegister(25, 8, 7)
left.shift_out(0)
mid.shift_out(0)
right.shift_out(0)

start = time.time()
stop = start + (10 * 600)


while time.time() < stop:
    left.shift_out(255)
    mid.shift_out(255)
    right.shift_out(255)

    if OUTPUT_ENABLE.is_active:
        OUTPUT_ENABLE.off()
    else:
        OUTPUT_ENABLE.on()


    time.sleep(1)


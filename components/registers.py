from loguru import logger

from ..utilities import (
    asynch,
    braille,
    events,
)
from ..utilities.register import (
    ShiftRegister,
)

left = ShiftRegister(17, 27, 22)
mid = ShiftRegister(10, 9, 11)
right = ShiftRegister(25, 8, 7)
registers = (left, mid, right)

is_active = False
text = ""
braille_lines: list[list[int]] = []
row_idx = 0
col_idx = 0
size = 3

has_processed = False

COUNTER_MAX = 300  # Seconds
# COUNTER_MAX = 5
COUNTER_MAX = 60
COUNTER_MAX = 120
counter = COUNTER_MAX
has_deactivated_by_counter = False


@asynch.periodic(1)
def cycle_counter():
    global counter, has_deactivated_by_counter
    if is_active:
        counter -= 1
        counter = max(0, counter)

        if (counter == 0) and (
            not has_deactivated_by_counter
        ):
            logger.warning(
                "Register timeout"
            )
            has_deactivated_by_counter = (
                True
            )
            events.OUTPUT_TOGGLE.publish(
                None
            )
    else:
        counter += 1
        counter = min(COUNTER_MAX, counter)

        has_deactivated_by_counter = False


def display():
    global braille_lines, row_idx, col_idx  # Should be unnecessary...

    try:
        if counter == 0:
            raise Exception()

        try:
            l = braille_lines[row_idx][
                col_idx + 0
            ]
        except:
            l = 0
        try:
            m = braille_lines[row_idx][
                col_idx + 1
            ]
        except:
            m = 0
        try:
            r = braille_lines[row_idx][
                col_idx + 2
            ]
        except:
            r = 0
    except:
        l = m = r = 0

    left.value = ~l
    mid.value = ~m
    right.value = ~r
    # left.value = ~0b0_000001_0
    # mid.value = ~0b0_000001_0
    # right.value = ~0b0_000001_0

    logger.debug(
        f"{row_idx} {col_idx} {l:0>8b} {m:0>8b} {r:0>8b}"
    )


def disable():
    global is_active, text

    for reg in registers:
        reg.value = 0
        reg.is_active = False
    is_active = False
    text = ""


@events.SHUTDOWN.subscribe
async def on_shutdown(*_):
    disable()


@events.WAITING_FOR_DOCUMENT.subscribe
async def on_waiting_for_document(*_):
    global has_processed

    disable()
    has_processed = False


@events.OUTPUT_BRAILLE.subscribe
async def on_output_braille(
    incoming_text: str,
):
    global is_active, text, braille_lines, row_idx, col_idx, has_processed

    logger.info("Braille output active.")

    for reg in registers:
        reg.is_active = True
    is_active = True
    text = incoming_text

    if not has_processed:
        logger.info(
            "Converting text to braille. . ."
        )
        braille_lines = [
            braille.text_to_braille(line)
            for line in text.split("\n")
        ]
        logger.info(
            "Converted text to braille."
        )
        has_processed = True

    else:
        logger.info(
            "Reusing previous braille conversion. . ."
        )
    row_idx = 0
    col_idx = 0

    logger.debug(braille_lines)

    display()
    events.OUTPUT_DISPLAY.publish(None)


@events.OUTPUT_TOGGLE.subscribe
async def on_output_toggle(*_):
    global is_active, text

    if not is_active:
        return

    logger.info("Braille output inactive.")
    stored_text = text
    disable()

    await asynch.sleep(
        0.5
    )  # Race conditions...
    events.OUTPUT_TTS.publish(stored_text)


@events.BUTTON_YELLOW_LEFT.subscribe
async def on_left_yellow_button(*_):
    global is_active, col_idx

    if not is_active:
        return

    if col_idx == 0:
        pass  # When already at line start, do nothing
    else:
        col_idx -= 3
        col_idx = max(col_idx, 0)

    display()


@events.BUTTON_YELLOW_RIGHT.subscribe
async def on_right_yellow_button(*_):
    global is_active, braille_lines, row_idx, col_idx, size

    if not is_active:
        return

    col_idx += 3
    if col_idx > (
        len(braille_lines[row_idx]) - 1
    ):
        col_idx -= 3

    # end_idx = len(braille_lines[row_idx]) - size
    # if col_idx == end_idx:
    #     pass  # When already at line end, do nothing
    # else:
    #     col_idx += 1

    display()


@events.BUTTON_WHITE_LEFT.subscribe
async def on_left_white_button(*_):
    global is_active, col_idx, row_idx

    if not is_active:
        return

    if row_idx == 0:
        pass  # When already at first line, do nothing
    else:
        row_idx -= 1
        col_idx = 0  # Reset to line start on every line change

    display()


@events.BUTTON_WHITE_RIGHT.subscribe
async def on_right_white_button(*_):
    global is_active, braille_lines, col_idx, row_idx

    if not is_active:
        return

    if row_idx == (len(braille_lines) - 1):
        pass  # When already at last line, do nothing
    else:
        row_idx += 1
        col_idx = 0  # Reset to line start on every line change

    display()

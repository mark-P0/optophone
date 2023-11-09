from ..components import registers
from ..components.buttons import power as power_button
from ..components.buttons.white import left as white_left
from ..components.buttons.white import right as white_right
from ..components.buttons.yellow import left as yellow_left
from ..components.buttons.yellow import right as yellow_right
from ..utilities import events

events.OUTPUT_BRAILLE.publish(
    'abcdefghijklmnopqrstuvwxyz'
    # '      '
    # 'aaaaaa'
)

events.loop.run_forever()
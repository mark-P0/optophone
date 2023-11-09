from ..components import registers, speakers
from ..components.buttons import power as power_button
from ..components.buttons import toggle
from ..components.buttons.white import left as white_left
from ..components.buttons.white import right as white_right
from ..components.buttons.yellow import left as yellow_left
from ..components.buttons.yellow import right as yellow_right
from ..components.leds import status
from ..utilities import events

events.OUTPUT_TTS.publish(
    'abcdefghijklmnopqrstuvwxyz'
    # '      '
    # 'aaaaaa'
)

events.loop.run_forever()
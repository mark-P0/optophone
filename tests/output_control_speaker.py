# flake8: noqa: F401 - Imported modules have event listeners that must be "executed" (via the act of importing)
# cspell: disable

import textwrap as tw

from ..components import speakers
from ..components.buttons import power as power_button
from ..components.buttons.white import left as white_left
from ..components.buttons.white import right as white_right
from ..components.buttons.yellow import left as yellow_left
from ..components.buttons.yellow import right as yellow_right
from ..utilities import events

_ = tw.dedent(
    """
    Mummy don't know daddy's getting hot,
    At the body shop, doing something unholy.
    A lucky, lucky girl,
    She got married to a boy like you.
    She'd kick you out if she ever, ever knew.
    'Bout all the - you tell me that you do.
    Dirty, dirty boy,
    You know everyone is talking on the scene,.
    I hear them whispering 'bout the places that you've been.
    And how you don't know how to keep your business clean.
    """
).strip()
events.OUTPUT_TTS.publish(_)

# events.OUTPUT_TTS.publish('Ang mga lugar ay pawang mga lugar lamang')
# events.OUTPUT_TTS.publish('Kung bibitaw nang mahinahon ako ba ay lulubayan ng aking mga kahapon na hindi na kayang ayusin pa ng lambing?')
# events.OUTPUT_TTS.publish('The quick brown fox jumps over the lazy dog')

events.loop.run_forever()

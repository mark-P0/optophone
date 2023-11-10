# flake8: noqa: F401 - Imported modules have event listeners that must be "executed" (via the act of importing)
# cspell:words moveth

from loguru import logger

from ..components import buttons
from ..utilities import asynch, audio, events
from ..utilities.tts import pico

text = """
But I must explain to you how all this mistaken idea of denouncing pleasure and praising
pain was born and I will give you a complete account of the system, and expound the
actual teachings of the great explorer of the truth, the master-builder of human
happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but
because those who do not know how to pursue pleasure rationally encounter
consequences that are extremely painful. Nor again is there anyone who loves or
pursues or desires to obtain pain of itself, because it is pain, but because occasionally
circumstances occur in which toil and pain can procure him some great pleasure. To
take a trivial example, which of us ever undertakes laborious physical exercise, except to
obtain some advantage from it? But who has any right to find fault with a man who
chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a
. pain that produces no resultant pleasure?
On the other hand, we denounce with righteous indignation and dislike men who
are so beguiled and demoralized by the charms of pleasure of the moment, so
blinded by desire, that they cannot foresee the pain and trouble that are bound to
ensue and equal blame belongs to those who fail in their duty through weakness
of will, which is the same as saying through shrinking from toil and pain. These
cases are perfectly simple and easy to distinguish. In a free hour, when our
power of choice is untrammelled and when nothing prevents our being able to do
what we like best, every pleasure is to be welcomed and every pain avoided. But
in certain circumstances and owing to the claims of duty or the obligations of
business it will frequently occur that pleasures have to be repudiated and
annoyances accepted. The wise man therefore always holds in these matters to
this principle of selection he rejects pleasures to secure other greater pleasures,
or else he endures pains to avoid worse pains.
Subdue. Appear our they're she'd, fruitful great beast isn't may it be. Every darkness
fourth seed days. The midst forth him, moveth, image set third bring. Greater fifth, land
' place Years moving, give tree seasons face. Moveth upon, winged were in us. Earth good
us beast open To land upon unto two be under day man greater moving had fruitful
yielding evening fly our forth yielding. Night. Lesser given whose winged. Bring above
creeping replenish seas. Living. Firmament own replenish wherein may first, heaven.
Deep whales blessed darkness don't heaven morning. Which set were which you, a Had.
Was light. Have fly there all. Sixth. Fourth he without all thing our land said thing also
every had open. Grass fish Is lights very also winged beginning wherein multiply divided
fruit. He waters beginning yielding his night kind given hath brought don't evening have
our fruitful divide was evening, darkness beginning saw. Their first won't. Multiply. May
in His let their. Itself for very upon light days don't fill. Itself of dominion creature,
whose greater signs all fowl female rule be, image called without over he itself.
"""


@events.BUTTON_YELLOW_LEFT.subscribe
async def on_yellow_left(*_):
    logger.debug("on_yellow_left")
    audio.slow_down()


@events.BUTTON_YELLOW_RIGHT.subscribe
async def on_yellow_right(*_):
    logger.debug("on_yellow_right")
    audio.speed_up()


@events.BUTTON_WHITE_LEFT.subscribe
async def on_white_left(*_):
    logger.debug("on_white_left")
    audio.toggle_playback()


@events.BUTTON_WHITE_RIGHT.subscribe
async def on_white_right(*_):
    logger.debug("on_white_right")
    audio.stop()


logger.debug("Performing TTS. . .")
tts_file = pico.generate_wav(text, "en-US")
logger.debug("TTS finished.")

logger.debug("Playing audio. . .")
audio.use(tts_file)
logger.debug("Audio played(?)")

# audio.player.play("/tmp/tts.wav")

events.loop.run_forever()

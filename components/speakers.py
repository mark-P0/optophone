"""
- Power to speakers should just depend on LED strip for sake of simplicity
- Both are tied to USB power
- When USB power is disabled, both components are disabled
"""
# flake8: noqa: E722 - Allow bare excepts...

from langdetect import DetectorFactory
from langdetect import detect as detect_lang
from loguru import logger

from ..utilities import asynch, audio, events
from ..utilities.tts import pico

DetectorFactory.seed = 0  # For deterministic results

is_active = False
text = ""

has_processed = False


def disable():
    global is_active, text

    if is_active:
        audio.stop()
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


@events.OUTPUT_TTS.subscribe
async def on_output_tts(incoming_text: str):
    global is_active, text, has_processed

    logger.info("Speakers active.")
    is_active = True
    text = incoming_text

    # logger.warning("Speakers not yet implemented!")
    # return

    # has_processed = True

    # logger.info("Performing TTS. . .")
    # filename = pico.generate_wav(text)
    # logger.info("TTS finished.")

    # logger.info("Playing audio. . .")
    # audio.use(filename)

    # return

    if not has_processed:
        has_processed = True

        logger.info("Performing TTS. . .")
        try:
            language = detect_lang(text)
        except:
            language = "en"
        logger.debug(f"{language=}")

        if language == "tl":
            filename = pico.generate_wav(text, "es-ES")
        else:
            filename = pico.generate_wav(text, "en-US")
        logger.info("TTS finished.")

        logger.info("Playing audio. . .")
        audio.use(filename)
    else:
        logger.info("Reusing previous TTS results. . .")
        audio.toggle_playback()

    events.OUTPUT_DISPLAY.publish(None)


@events.OUTPUT_TOGGLE.subscribe
async def on_output_toggle(*_):
    global is_active, text

    if not is_active:
        return

    logger.info("Speakers inactive.")
    stored_text = text
    disable()

    await asynch.sleep(0.5)  # Race conditions...
    events.OUTPUT_BRAILLE.publish(stored_text)


@events.BUTTON_YELLOW_LEFT.subscribe
async def on_yellow_left(*_):
    if not is_active:
        return

    logger.info("Playback slowed down.")
    audio.slow_down()


@events.BUTTON_YELLOW_RIGHT.subscribe
async def on_yellow_right(*_):
    if not is_active:
        return

    logger.info("Playback sped up.")
    audio.speed_up()


@events.BUTTON_WHITE_LEFT.subscribe
async def on_white_left(*_):
    if not is_active:
        return

    logger.info("Playback toggled.")
    audio.toggle_playback()


@events.BUTTON_WHITE_RIGHT.subscribe
async def on_white_right(*_):
    if not is_active:
        return

    logger.info("Playback stopped.")
    audio.stop()

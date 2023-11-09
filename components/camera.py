import time
from io import BytesIO

from loguru import logger
from picamera import PiCamera
from PIL import Image

from ..utilities import asynch, events, ocr
from .leds import strip


def capture_image(resolution=(1920, 1440)):
    """
    https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-to-a-pil-image
    """

    ## Create in-memory stream
    stream = BytesIO()

    ## Capture image with Picamera to stream
    camera = PiCamera()
    camera.resolution = resolution
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format="jpeg")

    camera.stop_preview()
    camera.close()

    ## "Rewind" stream to start so PIL can read its content
    stream.seek(0)
    return Image.open(stream)


@events.SHUTDOWN.subscribe
async def on_shutdown(*_):
    strip.on()


@events.WAITING_FOR_DOCUMENT.subscribe
async def on_waiting_for_document(*_):
    strip.off()


@events.DOCUMENT_FOUND.subscribe
async def on_document_found(*_):
    logger.info("Capturing image...")

    strip.on()
    image = capture_image()
    logger.info("Image captured.")
    strip.off()

    tmp_raw = "/tmp/1raw.jpeg"
    image.save(tmp_raw)
    logger.debug(f"Saved `{tmp_raw}`")

    await asynch.sleep(0.25)
    strip.on()

    events.IMAGE_CAPTURED.publish(image)


@events.IMAGE_CAPTURED.subscribe
async def on_image_capture(
    image: Image.Image,
):
    logger.info(
        "Performing OCR on image..."
    )

    try:
        text = ocr.image_to_text(image)
        logger.info("OCR finished.")
        logger.debug(text)
    except Exception as error:
        logger.warning(
            "OCR failed; timeout? non-document?"
        )
        logger.warning(error)
        text = ""

    events.OUTPUT_TTS.publish(
        text
    )  # Choose which of these is default...
    # events.OUTPUT_BRAILLE.publish(text)


if __name__ == "__main__":
    logger.add("/tmp/{time}.log")

    def loop():
        events.DOCUMENT_FOUND.publish(None)
        events.loop.run_forever()

    loop()
    breakpoint()

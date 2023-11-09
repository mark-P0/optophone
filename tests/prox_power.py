from ..components import prox
from ..components.buttons import power
from ..components.leds import status
from ..utilities import events


@events.DOCUMENT_FOUND.subscribe
async def on_document_found(*_):
    events.OUTPUT_TTS.publish('')

@events.WAITING_FOR_DOCUMENT.subscribe
async def on_document_wait(*_):
    events.OUTPUT_DISPLAY.publish('')

events.loop.run_forever()


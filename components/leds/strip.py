"""
Actually toggles full USB power
"""


from ...utilities import usb


def on():
    usb.on()


def off():
    usb.off()


# @events.WAITING_FOR_DOCUMENT.subscribe
# async def on_waiting_for_document(*_):
#     off()
#
#
# @events.DOCUMENT_FOUND.subscribe
# async def on_document_found(*_):
#     on()
#
#
# @events.IMAGE_CAPTURED.subscribe
# async def on_image_captured(*_):
#     off()
#
#     await asynch.sleep(0.5)
#
#     on()  # Leave LED strip on after image capture


if __name__ == "__main__":
    breakpoint()
"""
Managed via the entrypoint shell script
"""

# from loguru import logger
#
# from ...utilities import events
# from ...utilities.cli import ColorAffix, color_text
#
#
# @events.SHUTDOWN.subscribe
# async def on_shutdown(*_):
#     text = color_text("OFF", (ColorAffix.FG_RED, ColorAffix.BG_BLACK))
#     logger.debug(f"Power LED: {text}")
#
#
# @events.POWERUP.subscribe
# async def on_powerup(*_):
#     text = color_text("ON", (ColorAffix.BG_RED, ColorAffix.FG_WHITE))
#     logger.debug(f"Power LED: {text}")

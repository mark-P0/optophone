from mpv import MPV


player = MPV(keep_open=True)

SPEED_STEP = 0.25
SPEED_MIN = 0.25
SPEED_MAX = 2.00


def slow_down():
    player.speed = max(
        (
            SPEED_MIN,
            player.speed - SPEED_STEP,
        )
    )


def speed_up():
    player.speed = min(
        (
            SPEED_MAX,
            player.speed + SPEED_STEP,
        )
    )


def reset():
    player.seek(0, "absolute")


def toggle_playback():
    if player.eof_reached:
        reset()
    player.pause = not player.pause


def play():
    player.pause = False


def pause():
    player.pause = pause


def stop():
    player.pause = True
    reset()


def use(filename: str):
    player.play(filename)
    play()

width = 0


def oneline(item, cursor_on_end=True):
    global width

    string = str(item)
    width = max(width, len(string))
    string = f"{string:<{width}}"

    if cursor_on_end:
        print(f"\r{string}", end="", flush=True)
    else:
        print(string, end="\r", flush=True)


if __name__ == "__main__":
    import time

    for fn in (
        lambda: oneline(0.1234),
        lambda: oneline(0.1234, cursor_on_end=False),
    ):
        fn()
        time.sleep(1)

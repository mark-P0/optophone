# fmt:off
letters = {
    "a": 0b0_000001_0, "b": 0b0_000011_0,
    "c": 0b0_001001_0, "d": 0b0_011001_0,
    "e": 0b0_010001_0, "f": 0b0_001011_0,
    "g": 0b0_011011_0, "h": 0b0_010011_0,
    "i": 0b0_001010_0, "j": 0b0_011010_0,
    "k": 0b0_000101_0, "l": 0b0_000111_0,
    "m": 0b0_001101_0, "n": 0b0_011101_0,
    "o": 0b0_010101_0, "p": 0b0_001111_0,
    "q": 0b0_011111_0, "r": 0b0_010111_0,
    "s": 0b0_001110_0, "t": 0b0_011110_0,
    "u": 0b0_100101_0, "v": 0b0_100111_0,
    "w": 0b0_111010_0, "x": 0b0_101101_0,
    "y": 0b0_111101_0, "z": 0b0_110101_0}

numbers = {
    "0": 0b0_011010_0, "1": 0b0_000001_0,
    "2": 0b0_000011_0, "3": 0b0_001001_0,
    "4": 0b0_011001_0, "5": 0b0_010001_0,
    "6": 0b0_001011_0, "7": 0b0_011011_0,
    "8": 0b0_010011_0, "9": 0b0_001010_0}

special = {
    " ":  0b0_000000_0, ",": 0b0_000010_0,
    ";":  0b0_000110_0, ":": 0b0_010010_0,
    ".":  0b0_110010_0, "?": 0b0_100110_0,
    "!":  0b0_010110_0, '"': 0b0_110110_0,
    "'":  0b0_100110_0, "(": 0b0_100011_0,
    ")":  0b0_011100_0, "/": 0b0_001100_0,
    "\\": 0b0_100001_0, "-": 0b0_100100_0}

prefixes = {
    "capital": 0b0_100000_0, "number": 0b0_111100_0,
    "quote":   0b0_000100_0, "paren":  0b0_010000_0,
    "slash":   0b0_111000_0}
# fmt:on


def text_to_braille(text: str):
    for char in text:
        if char.lower() in letters:
            if char.isupper():
                yield prefixes["capital"]
            yield letters[char.lower()]

        elif char in numbers:
            yield prefixes["number"]
            yield numbers[char]

        elif char in special:
            if char == '"' or char == "'":
                yield prefixes["quote"]
            elif char == "(" or char == ")":
                yield prefixes["parenthesis"]
            elif char == "/" or char == "\\":
                yield prefixes["slash"]
            yield special[char]

        else:
            yield special[" "]


if __name__ == "__main__":
    # fmt: off

    print(
        text_to_braille(
            "This is a sample text."
        )
    )
    print(
        [
            bin(_)
            for _ in text_to_braille(
                "This is a sample text."
            )
        ]
    )

    # from_string("This is a sample text.")
    # from_string(
    #     """1) Shakespeare's line "to be or not to be" is usually interpreted as meaning "is it better to live or to die?"."""
    # )

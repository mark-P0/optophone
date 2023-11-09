"""
String operations to improve OCR results
"""


def remove_blank_lines(string: str) -> str:
    return "\n".join(
        line
        for line in string.splitlines()
        if line != ""
    )

import pytesseract as tess
from loguru import logger
from PIL import Image

from . import conversions, postprocessing, preprocessing


def preprocess(image: Image.Image) -> Image.Image:
    img_mat = conversions.pil_to_cv(image)
    img_mat = preprocessing.dewarp(img_mat)
    image = conversions.cv_to_pil(img_mat)
    image = preprocessing.correct_orientation(image)
    return image


def postprocess(text: str) -> str:
    text = postprocessing.remove_blank_lines(text)
    return text


def image_to_text(image: Image.Image) -> str:
    image = preprocess(image)

    tmp_preproc = "/tmp/2preproc.jpeg"
    image.save(tmp_preproc)
    logger.debug(f"Saved `{tmp_preproc}`")

    config_map = {
        "tessedit_char_whitelist": '"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.?!\'-()/1234567890"',
        "tessedit_write_images": "true",
    }
    config = " ".join(f"-c {key}={value}" for key, value in config_map.items())

    text = tess.image_to_string(image, lang="eng+fil", config=config, timeout=60)
    text = postprocess(text)

    return text

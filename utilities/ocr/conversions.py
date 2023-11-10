import cv2 as cv
import numpy as np
from PIL import Image


def pil_to_cv(img: Image.Image) -> cv.Mat:
    """
    i.e. convert RGB to BGR

    - https://stackoverflow.com/q/14134892
    - https://stackoverflow.com//14556545/
    """
    mat = np.array(img)
    ##         Rw Cl RGB
    return mat[:, :, ::-1]


def cv_to_pil(img: cv.Mat) -> Image.Image:
    return Image.fromarray(img)

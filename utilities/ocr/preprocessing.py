"""
Image operations to prepare for OCR
"""

import cv2 as cv
import numpy as np
import pytesseract as tess
from loguru import logger
from PIL import Image


def get_osd(img: Image.Image) -> dict[str, str]:
    raw = tess.image_to_osd(img)
    return dict(line.split(": ") for line in raw.splitlines())


def correct_orientation(
    img: Image.Image,
) -> Image.Image:
    logger.debug("Fixed rotation by -90")
    return img.rotate(-90, expand=True)

    # osd = get_osd(img)
    # rotation = -float(osd["Rotate"])
    # logger.debug(f"{rotation=}")
    # return img.rotate(rotation, expand=True)


def reorder_points(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    order_by_x = sorted(points, key=lambda point: point[0])
    order_by_y = sorted(points, key=lambda point: point[1])

    x_left = [x for x, y in order_by_x[:2]]
    x_right = [x for x, y in order_by_x[2:]]

    y_top = [y for x, y in order_by_y[:2]]
    y_bot = [y for x, y in order_by_y[2:]]

    top_left, *_ = [(x, y) for x, y in points if x in x_left and y in y_top]
    bot_left, *_ = [(x, y) for x, y in points if x in x_left and y in y_bot]
    bot_right, *_ = [(x, y) for x, y in points if x in x_right and y in y_bot]
    top_right, *_ = [(x, y) for x, y in points if x in x_right and y in y_top]

    return [top_left, bot_left, bot_right, top_right]


def dewarp(img_mat: cv.Mat) -> cv.Mat:
    """
    - Determine page boundaries
    - Approximate proper shape from boundaries
    - Produce approximated shape as output

    ---

    - https://stackoverflow.com/a/60941676
    - https://docs.opencv.org/4.7.0/da/d6e/tutorial_py_geometric_transformations.html
    """

    ## Transform to grayscale
    greyed_mat = cv.cvtColor(img_mat, cv.COLOR_BGR2GRAY)

    ## Binarize image via thresholding (Otsu)
    ## Blur image first to erode most text
    blurred_mat = cv.GaussianBlur(greyed_mat, (5, 5), 0)
    _, threshold_mat = cv.threshold(
        blurred_mat, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU
    )

    ## Apply morphology (close, then open)
    ##   to clean leftover page text
    kernel = np.ones((7, 7), np.uint8)
    morphed_mat = cv.morphologyEx(
        cv.morphologyEx(threshold_mat, cv.MORPH_CLOSE, kernel), cv.MORPH_OPEN, kernel
    )

    ## Find contours to isolate page
    ## Provides sequence of contours.
    contours, _ = cv.findContours(morphed_mat, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    ### Find largest contour
    ### Needed in case several contours were detected
    largest_contour = max(contours, key=lambda c: cv.contourArea(c))

    ## Approximate page shape
    perimeter = cv.arcLength(largest_contour, True)
    epsilon = 10 / 100 * perimeter
    shape_corners = cv.approxPolyDP(largest_contour, epsilon, True)

    ## Normalize shape corners and set as base shape
    ## Currently: [[x, y], ...]`
    base_shape = reorder_points([corner[0] for corner in shape_corners])
    base_shape = np.array(base_shape, np.float32)

    ## Compute properties of target shape
    ## Corner points ordered CCW from top-left
    (top_left, bot_left, bot_right, top_right) = base_shape
    width_top = top_right[0] - top_left[0]
    width_bot = bot_right[0] - bot_left[0]
    height_left = bot_left[1] - top_left[1]
    height_right = bot_right[1] - top_right[1]

    ### Width, height naively computed as average of corresponding sides...
    width = (width_top + width_bot) / 2
    height = (height_left + height_right) / 2

    target_shape = [  # Also arranged CCW-TL
        [0, 0],
        [0, height],
        [width, height],
        [width, 0],
    ]
    target_shape = np.array(target_shape, np.float32)

    ## Transform base shape into target shape
    M = cv.getPerspectiveTransform(base_shape, target_shape)
    warped_mat = cv.warpPerspective(img_mat, M, (int(width), int(height)))

    return warped_mat


if __name__ == "__main__":
    breakpoint()

"""Helper Functions"""

import numpy as np
from PIL import Image


def load_target_image(image_path, gray=False, size: None | int | tuple[int, int]=None):
    """Loads images from image path.

    Loads and converts image to given colorspace for later processing using
    OpenCV. Attempts to resize image if size is provided.

    Args:
        image_path (str): path to load the image.
        gray (bool): if True the image is loaded as grayscale, if False rgb.
            Defaults to False.
        size (tuple or int): size of target image as (width, height), or width
            and preserve aspect ratio. If None, then original image dimension is
            kept.

    Returns:
        Image loaded from the path as a numpy.ndarray.
    """
    target = Image.open(image_path)

    if gray:
        target = target.convert("L")
    else:
        target = target.convert("RGB")

    if isinstance(size, int):
        width = size
        height = int(size * target.height / target.width)
        target = target.resize((width, height))
    elif isinstance(size, tuple):
        target = target.resize(size)

    return np.array(target, dtype=np.uint8)


def show_image(img_arr):
    """Displays image on window.

    Arguments:
        img_arr (numpy.ndarray): image array to be displayed
    """
    img = Image.fromarray(img_arr)
    img.show()

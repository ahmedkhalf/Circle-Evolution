"""Helper Functions"""
import os

import cv2

import matplotlib.pyplot as plt


def load_target_image(image_path, color=True, size=None):
    """Loads images from image path.

    Loads and converts image to given colorspace for later processing using
    OpenCV. Attempts to resize image if size is provided.

    Args:
        image_path (str): path to load the image.
        color (bool): if true the image is loaded as rgb, if false grayscale.
            Defaults to true.
        size (tuple): size of target image as (height, width). If None, then
            original image dimension is kept.

    Returns:
        Image loaded from the path as a numpy.ndarray.

    Raises:
        FileNotFoundError: image_path does not exist.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image was not found at {image_path}")

    if color:
        target = cv2.imread(image_path, cv2.IMREAD_COLOR)
        # Switch from bgr to rgb
        target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    else:
        target = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if size:
        # Only resizes image if it is needed!
        target = cv2.resize(src=target, dsize=size, interpolation=cv2.INTER_AREA)
    return target

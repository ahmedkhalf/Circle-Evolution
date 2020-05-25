"""Helper Functions"""
import os

import cv2

import matplotlib.pyplot as plt


def load_target_image(image_path, color=cv2.COLOR_BGR2GRAY, size=None):
    """Loads images from image path.

    Loads and converts image to given colorspace for later processing using
    OpenCV. Attempts to resize image if size is provided.

    Args:
        image_path (str): path to load the image.
        color: optional variable for colorspace conversion

    Returns:
        Image loaded from the path as a numpy.ndarray.

    Raises:
        FileNotFoundError: image_path does not exist.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image was not found at {image_path}")
    img = cv2.imread(image_path)
    # Performs Image Convertion
    target = cv2.cvtColor(img, color)
    if size:
        # Only resizes image if it is needed!
        target = cv2.resize(src=target, dsize=size, interpolation=cv2.INTER_AREA)
    return target


def show_image(img_arr):
    """Displays image on window.

    Arguments:
        img_arr (numpy.ndarray): image array to be displayed
    """
    plt.figure()
    plt.axis("off")
    plt.imshow(img_arr, cmap="gray", vmin=0, vmax=255)
    plt.show()

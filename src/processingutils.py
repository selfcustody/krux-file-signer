"""
processingutils.py

Optional video frame post-processing helpers.
"""

import cv2

from logutils import verbose_log


def normalization_transform(frame, verbose: bool = False):
    """
    Normalize `frame` in place; cameras vary in contrast and brightness.

    @see https://stackoverflow.com/questions/61016954/
    controlling-contrast-and-brightness-of-video-stream-in-opencv-and-python
    """
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    if verbose:
        verbose_log(f"normalized (frame={frame})")


def gray_transform(frame, verbose: bool = False):
    """Return a grayscale copy of `frame`."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if verbose:
        verbose_log(f"gray scale (frame={gray})")
    return gray

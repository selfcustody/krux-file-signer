"""
processingutils.py

Optional video frame post-processing helpers.
"""

import logging

import cv2

log = logging.getLogger(__name__)


def normalization_transform(frame):
    """
    Normalize `frame` in place; cameras vary in contrast and brightness.

    @see https://stackoverflow.com/questions/61016954/
    controlling-contrast-and-brightness-of-video-stream-in-opencv-and-python
    """
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    log.debug("normalized (frame=%s)", frame)


def gray_transform(frame):
    """Return a grayscale copy of `frame`."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    log.debug("gray scale (frame=%s)", gray)
    return gray

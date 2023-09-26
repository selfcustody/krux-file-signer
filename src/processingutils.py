#######################
# Third party libraries
#######################
import cv2

#################
# Local libraries
#################
from logutils import verbose_log


def normalization_transform(**kwargs):
    """ "
    Apply Gray scale on frames

    Kwargs
        :param frame
            The frame which will be applyed the transformation
        :param verbose
            Apply verbose messages
    """
    frame = kwargs.get("frame")
    verbose = kwargs.get("verbose")

    # Cameras have different configurations
    # and behaviours, so try apply some normalization
    # @see https://stackoverflow.com/questions/61016954/
    # controlling-contrast-and-brightness-of-video-stream-in-opencv-and-python
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

    # Verbose some data
    if verbose:
        verbose_log(f"normalized (frame={frame})")


def gray_transform(**kwargs):
    """ "
    Apply Gray scale on frames

    Kwargs
        :param ret
        :param frame
            The frame which will be applyed the transformation
        :param verbose
            Apply verbose messages
    """
    frame = kwargs.get("frame")
    verbose = kwargs.get("verbose")

    # Convert frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # verbose_loge some data
    if verbose:
        verbose_log(f"gray scale (frame={frame})")

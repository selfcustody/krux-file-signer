"""
videoutils.py

some video utilities to scan and post processing
images. 

TODO: unify processingutils.py to this file?
"""
####################
# Standard libraries
####################
import base64

#######################
# Thrid party libraries
#######################
import cv2

#################
# Local libraries
#################
from utils.log import now


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

    # Cameras have different configurations
    # and behaviours, so try apply some normalization
    # @see https://stackoverflow.com/questions/61016954/
    # controlling-contrast-and-brightness-of-video-stream-in-opencv-and-python
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

    # Verbose some data


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

    # Convert frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def scan(**kwargs) -> str:
    """
    Opens a scan window and uses cv2 to detect
    and decode a QR code, returning its data.
    Can be applyed some normalization
    or gray scale

    Kwargs:
        :is_normalized
            Apply some normalization
        :is_gray_scale
            Apply some gray scale
        :param verbose
            Apply or not verify
    """
    verbose = kwargs.get("versbose")
    is_normalized = kwargs.get("is_normalized")
    is_gray_scale = kwargs.get("is_gray_scale")

    vid = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    qr_data = None
    while True:
        # Capture the video frame by frame
        # use some dummy vars (__+[a-zA-Z0-9]*?$)
        # to avoid the W0612 'Unused variable' pylint message
        _ret, frame = vid.read()

        # Apply some normalization if wanted
        if is_normalized:
            normalization_transform(frame=frame, verbose=verbose)

        # Apply gray scale if wanted
        if is_gray_scale:
            gray_transform(frame=frame)

        # Detect qrcode
        qr_data, _bbox, _straight_qrcode = detector.detectAndDecode(frame)

        # Verify null data
        if len(qr_data) > 0:
            break

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    vid.release()
    cv2.destroyAllWindows()

    return qr_data


def scan_and_save_signature(**kwargs):
    """
    Scan with camera the generated signatue

    Kwargs:
        :is_normalized
            Apply normalization on video
        :is_gray_scale
            Apply some gray scale on video
        :param verbose
    """
    is_normalized = kwargs.get("is_normalized")
    is_gray_scale = kwargs.get("is_gray_scale")
    filename = kwargs.get("filename")

    _ = input(f"[{now()}] Press enter to scan signature")
    signature = scan(
        is_normalized=is_normalized,
        is_gray_scale=is_gray_scale,
    )

    # Encode data
    binary_signature = base64.b64decode(signature.encode())

    # Saves a signature
    signature_file = f"{filename}.sig"
    with open(signature_file, "wb") as sig_file:
        sig_file.write(binary_signature)


def scan_public_key(**kwargs) -> str:
    """
    Scan with camera the generated public key

    Kwargs:
        :is_normalized
            Apply or not normalization on image
        :is_gray_scale
            Apply or not gray scale on image
        :param verbose
    """
    is_normalized = kwargs.get("is_normalized")
    is_gray_scale = kwargs.get("is_gray_scale")

    _ = input(f"[{now()}] Press enter to scan public key")
    public_key = scan(
        is_normalized=is_normalized,
        is_gray_scale=is_gray_scale,
    )

    return public_key

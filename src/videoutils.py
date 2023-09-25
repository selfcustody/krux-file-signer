#######################
# Thrid party libraries
#######################
import cv2

#################
# Local libraries
#################
from logutils import *
from processingutils import *

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

    verbose_log("Opening camera")
    vid = cv2.VideoCapture(0)

    verbose_log("Starting detection")
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

        # Verbose some data
        if verbose:
            verbose_log(f"reading (qr_data={qr_data})")
            verbose_log(f"reading (_bbox={_bbox}")
            verbose_log(f"reading (_straight_qrcode={_straight_qrcode})")

        # Verify null data
        if verbose:
            verbose_log(f"len(qr_data) = {len(qr_data)}")

        if len(qr_data) > 0:
            break

        # Display the resulting frame
        if verbose:
            verbose_log(f"Showing (frame={frame})")

        # Show image
        cv2.imshow("frame", frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if verbose:
                verbose_log("quiting QRCode detection...")
            break

    # After the loop release the cap object
    if verbose:
        verbose_log("Releasing video...")

    vid.release()

    # Destroy all the windows
    if verbose:
        verbose_log("Destroying all ksigner windows...")

    cv2.destroyAllWindows()

    return qr_data

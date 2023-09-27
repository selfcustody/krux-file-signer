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
from logutils import verbose_log, now
from processingutils import normalization_transform
from processingutils import gray_transform


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
    verbose = kwargs.get("verbose")
    filename = kwargs.get('filename')

    _ = input(f"[{now()}] Press enter to scan signature")
    signature = scan(
        is_normalized=is_normalized, is_gray_scale=is_gray_scale, verbose=verbose
    )

    # Encode data
    binary_signature = base64.b64decode(signature.encode())
    if verbose:
        verbose_log(f"Signature: {binary_signature}")

    # Saves a signature
    signature_file = f"{filename}.sig"
    verbose_log(f"Saving a signature file: {signature_file}")
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
    verbose = kwargs.get("verbose")

    _ = input(f"[{now()}] Press enter to scan public key")
    public_key = scan(
        is_normalized=is_normalized, is_gray_scale=is_gray_scale, verbose=verbose
    )

    if verbose:
        verbose_log(f"Public key: {public_key}")

    return public_key

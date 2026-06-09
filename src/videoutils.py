"""
videoutils.py

Utilities to scan QR codes from the camera.
"""

import base64

import cv2

from logutils import verbose_log, now
from processingutils import normalization_transform, gray_transform


def scan(
    is_normalized: bool = False,
    is_gray_scale: bool = False,
    verbose: bool = False,
) -> str:
    """
    Open the camera and return the data of the first QR code detected.
    Press 'q' to abort.
    """
    verbose_log("Opening camera")
    vid = cv2.VideoCapture(0)

    verbose_log("Starting detection")
    detector = cv2.QRCodeDetector()

    qr_data = ""
    while True:
        _ret, frame = vid.read()

        if is_normalized:
            normalization_transform(frame, verbose=verbose)
        if is_gray_scale:
            frame = gray_transform(frame, verbose=verbose)

        qr_data, _bbox, _straight = detector.detectAndDecode(frame)
        if verbose:
            verbose_log(f"reading (qr_data={qr_data}, len={len(qr_data)})")

        if len(qr_data) > 0:
            break

        cv2.imshow("frame", frame)
        # 'q' aborts the detection
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if verbose:
                verbose_log("quiting QRCode detection...")
            break

    vid.release()
    cv2.destroyAllWindows()
    return qr_data


def scan_and_save_signature(
    signature_file: str,
    is_normalized: bool = False,
    is_gray_scale: bool = False,
    verbose: bool = False,
):
    """Scan the signature QR code and save its bytes to `signature_file`."""
    input(f"[{now()}] Press enter to scan signature")
    signature = scan(
        is_normalized=is_normalized, is_gray_scale=is_gray_scale, verbose=verbose
    )

    binary_signature = base64.b64decode(signature.encode())
    if verbose:
        verbose_log(f"Signature: {binary_signature}")

    verbose_log(f"Saving a signature file: {signature_file}")
    with open(signature_file, "wb") as sig_file:
        sig_file.write(binary_signature)


def scan_public_key(
    is_normalized: bool = False,
    is_gray_scale: bool = False,
    verbose: bool = False,
) -> str:
    """Scan and return the public key QR code data."""
    input(f"[{now()}] Press enter to scan public key")
    public_key = scan(
        is_normalized=is_normalized, is_gray_scale=is_gray_scale, verbose=verbose
    )

    if verbose:
        verbose_log(f"Public key: {public_key}")
    return public_key

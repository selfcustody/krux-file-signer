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
import logging

#######################
# Thrid party libraries
#######################
import cv2

#################
# Local libraries
#################
from utils.log import now

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
    logging.debug('Starting OpenCV capture')
    vid = cv2.VideoCapture(0)

    logging.debug('Starting OpenSV QRCode detector')
    detector = cv2.QRCodeDetector()
    qr_data = None
    
    while True:
        # Capture the video frame by frame
        # use some dummy vars (__+[a-zA-Z0-9]*?$)
        # to avoid the W0612 'Unused variable' pylint message
        logging.debug('Waiting for data...')

        _ret, frame = vid.read()

        # Detect qrcode
        qr_data, _bbox, _straight_qrcode = detector.detectAndDecode(frame)

        # Verify null data
        if len(qr_data) > 0:
            logging.debug('QRCode detected')
            break

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord("q"):
            logging.debug("Key 'q' pressed: exiting")
            break

    logging.debug('Releasing video')
    vid.release()

    logging.debug('Destroying video window')
    cv2.destroyAllWindows()

    return qr_data


def scan_signature():
    """
    Scan with camera the generated signatue
    """
    
    _ = input(f"Press enter to scan signature")
    signature = scan()
    
    # Encode data
    logging.debug('Encoding signature')
    data = signature.encode()
    
    logging.debug(f'Signature (data={data})')
    return data


def scan_public_key(**kwargs) -> str:
    """
    Scan with camera the generated public key
    """
    _ = input(f"[{now()}] Press enter to scan public key")
    public_key = scan()

    logging.debug(f'Public Key (data={public_key})')
    return public_key

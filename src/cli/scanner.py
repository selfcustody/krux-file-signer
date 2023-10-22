"""
scanner.py

some video utilities to scan qrcodes. 
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
from utils.log import build_logger

class Scanner:
    """
    Scanner is the cli utility to scan
    Signature and PublicKey
    """
    def __init__(self, **kwargs):
        loglevel = kwargs.get('loglevel')
        self.log = build_logger(__name__, loglevel)

    def _scan(self) -> str:
        """
        Opens a scan window and uses cv2 to detect
        and decode a QR code, returning its data.
        Can be applyed some normalization
        or gray scale
        """
        self.log.debug('Starting OpenCV capture')
        vid = cv2.VideoCapture(0)

        self.log.debug('Starting OpenSV QRCode detector')
        detector = cv2.QRCodeDetector()
    
        qr_data = None
    
        while True:
            # Capture the video frame by frame
            # use some dummy vars (__+[a-zA-Z0-9]*?$)
            # to avoid the W0612 'Unused variable' pylint message
            self.log.debug('Waiting for data...')

            _ret, frame = vid.read()

            # delattrtect qrcode
            qr_data, _bbox, _straight_qrcode = detector.detectAndDecode(frame)

            # Verify null data
            if len(qr_data) > 0:
                self.log.debug('QRCode detected')
                break

            # Display the resulting frame
            cv2.imshow("frame", frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.log.debug("Key 'q' pressed: exiting")
                break

        self.log.debug('Releasing video')
        vid.release()

        self.log.debug('Destroying video window')
        cv2.destroyAllWindows()

        return qr_data

    def scan_signature(self) -> str:
        """
        Scan with camera the generated signatue
        """
    
        _ = input(f"Press enter to scan signature")
        signature = self._scan()
    
        # Encode data
        self.log.debug('Encoding signature')
        data = str.encode(signature)

        self.log.debug(f'Signature (data={data})')
        return data


    def scan_public_key(self) -> str:
        """
        Scan with camera the generated public key
        """
        _ = input(f"[{now()}] Press enter to scan public key")
        public_key = self._scan()

        self.log.debug(f'Public Key (data={public_key})')
        return public_key

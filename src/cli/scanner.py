# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
scanner.py

Export a :class:`Scanner` class to be used :class:`Signer` and :class:`Verifyer`.
To be used only with `ksigner-cli`.
"""
#######################
# Thrid party libraries
#######################
import cv2


class Scanner:
    """
    Scanner is the cli utility to scan signatures and public keys
    when user uses `ksigner-cli` utility.
    """

    def _scan(self) -> str:
        """
        Opens a scan window and uses cv2 to detect
        and decode a QR code, returning its data.
        Can be applyed some normalization
        or gray scale
        """
        vid = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        qr_data = None

        while True:
            # Capture the video frame by frame
            # use some dummy vars (__+[a-zA-Z0-9]*?$)
            # to avoid the W0612 'Unused variable' pylint message
            _ret, frame = vid.read()

            # delattrtect qrcode
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

    def scan_signature(self) -> str:
        """
        Scan with camera the generated signatue
        """
        _ = input("Press enter to scan signature")
        signature = self._scan()
        return signature

    def scan_public_key(self) -> str:
        """
        Scan with camera the generated public key
        """
        _ = input("Press enter to scan public key")
        public_key = self._scan()
        return public_key

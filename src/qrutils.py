"""
qrutils.py

Utilities to generate QR codes.
"""

import logging
from io import StringIO

from qrcode import QRCode

log = logging.getLogger(__name__)


def make_qr_code(data: str) -> str:
    """Return `data` encoded as an ASCII-art QR code."""
    log.debug("Adding (data=%s)", data)
    qr_code = QRCode()
    qr_code.add_data(data)

    qr_string = StringIO()
    qr_code.print_ascii(out=qr_string, invert=True)
    return qr_string.getvalue()

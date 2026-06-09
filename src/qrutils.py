"""
qrutils.py

Utilities to generate QR codes.
"""

from io import StringIO

from qrcode import QRCode

from logutils import verbose_log


def make_qr_code(data: str, verbose: bool = False) -> str:
    """Return `data` encoded as an ASCII-art QR code."""
    if verbose:
        verbose_log(f"Adding (data={data})")

    qr_code = QRCode()
    qr_code.add_data(data)

    qr_string = StringIO()
    qr_code.print_ascii(out=qr_string, invert=True)
    return qr_string.getvalue()

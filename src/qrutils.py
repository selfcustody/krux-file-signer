"""
qrutils.py

utils to generate QRcodes
"""
####################""
# Standart libraries
####################
from io import StringIO

#######################
# Thrid party libraries
#######################
from qrcode import QRCode

#################
# Local libraries
#################
from logutils import verbose_log


def make_qr_code(**kwargs) -> str:
    """
    Builds the ascii data to QR code

    Kwargs:
        :param data
            The data to be encoded in qrcode
        :param verbose
            Apply verbose or not
    """
    qr_data = kwargs.get("data")
    verbose = kwargs.get("verbose")

    qr_code = QRCode()

    if verbose:
        verbose_log("INFO", f"Adding (data={qr_data})")

    qr_code.add_data(qr_data)

    if verbose:
        verbose_log("INFO", "Converting data to ascii")

    qr_string = StringIO()
    qr_code.print_ascii(out=qr_string, invert=True)

    return qr_string.getvalue()


def make_qr_code_image(**kwargs) -> str:
    """
    Creates a QR code image

    Kwargs:
        :param data
            The data to be encoded in qrcode
        :param verbose
            Apply verbose or not
    """
    qr_data = kwargs.get("data")
    verbose = kwargs.get("verbose")

    qr_code = QRCode()

    if verbose:
        verbose_log("INFO", f"Adding (data={qr_data})")

    qr_code.add_data(qr_data)

    if verbose:
        verbose_log("INFO", "Creating image")

    qr_image = qr_code.make_image()
    return qr_image

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
    qr_code = QRCode()
    qr_code.add_data(qr_data)
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
    qr_code = QRCode()
    qr_code.add_data(qr_data)
    qr_image = qr_code.make_image()
    return qr_image

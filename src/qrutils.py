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
import pyqrcode

#################
# Local libraries
#################
from logutils import verbose_log

def encode_to_string(data):
    """
    Cloned from https://github.com/odudex/krux/blob/android/android/mocks/qrcode.py
    """
    
    #pre-decode if binary (Compact Seed QR)
    try:
        code_str = pyqrcode.create(data, error="L", mode="binary").text()
    except:
        # Try binary
        data = data.decode('latin-1')
        code_str = pyqrcode.create(data, error="L", mode="binary").text()
    # if len(data) in (48,96) and isinstance(data, str):  # Seed QR
    code_str = pyqrcode.create(data, error="L").text()
    # else:
    #     code_str = pyqrcode.create(data, error="M", mode="binary").text()
    size = 0
    while code_str[size] != "\n":
        size += 1
    i = 0
    padding = 0
    while code_str[i] != "1":
        if code_str[i] == "\n":
            padding += 1
        i += 1
    code_str = code_str[(padding) * (size + 1) : -(padding) * (size + 1)]
    size -= 2 * padding

    new_code_str = ""
    for i in range(size):
        for j in range(size + 2 * padding + 1):
            if padding <= j < size + padding:
                index = i * (size + 2 * padding + 1) + j
                new_code_str += code_str[index]
        new_code_str += "\n"

    return new_code_str

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

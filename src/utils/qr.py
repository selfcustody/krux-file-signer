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
qr.py

utility to generate QRcodes
"""
####################
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
    -------
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
    -------
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

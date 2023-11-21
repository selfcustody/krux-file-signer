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
verifyer.py

functions that use openssl as a wrapper
to verify signatures

TODO: replace for pyca/cryptography or pyOpenSSL 
"""

####################
# Standart libraries
####################
import os

#######################
# Third party libraries
#######################
# from OpenSSL.crypto import load_publickey, FILETYPE_PEM, verify, X509
from OpenSSL import crypto

#################
# Local libraries
#################
from cli.actioner import Actioner


class Verifyer(Actioner):
    """
    Verifyer is the class
    that manages the `verify` verify_openssl_command
    with given :param:`file`, :param:`pubkey` and
    :param:`signature`
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.file = os.path.abspath(kwargs.get("file"))
        self.pubkey = os.path.abspath(kwargs.get("pubkey"))
        self.signature = os.path.abspath(kwargs.get("signature"))

    def verify(self) -> str:
        """
        Use pyopenssl to verify a file with its signature and public key
        provided in class instantiation
        """
        msg = ""
        try:
            self.debug("Loading X509 object")
            x509 = crypto.X509()

            # load data
            self.debug("Loading file data")
            with open(self.file, "rb") as f_data:
                file_data = f_data.read()

            # load signature
            self.debug("Loading signature bytes")
            with open(self.signature, "rb") as f_data:
                signature = f_data.read()

            # load public key
            self.debug("Loading public key certificate")
            with open(self.pubkey, encoding="utf-8") as f_data:
                pubkey_data = f_data.read()

            pkey = crypto.load_publickey(crypto.FILETYPE_PEM, pubkey_data)
            x509.set_pubkey(pkey)

            # Now verify
            # According de documentation found in
            # https://pyopenssl.org/en/stable/api/crypto.html#OpenSSL.crypto.verify
            # it will return :data:`None` if signature is correct
            self.debug("Verifying...")
            crypto.verify(x509, signature, file_data, "sha256")
            msg = "Signature verified with success"

        # pylint: disable=broad-exception-caught
        except Exception as exc:
            msg = f"Something wrong is not correct:\n\t{exc}"

        return msg

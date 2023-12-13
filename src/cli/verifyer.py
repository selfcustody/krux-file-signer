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


Export a :class:`Verifyer` class to be used in `ksigner-cli` and
`ksigner-gui` during `verify` process.
"""

####################
# Standart libraries
####################
import os

#######################
# Third party libraries
#######################
from OpenSSL import crypto


class Verifyer:
    """
    Verifyer is the class
    that manages the `verify`

    Kwargs:
    -------

        :param:`file` the path of file to be verified
        :param:`pubkey` the path of public key file
        :param:`signature` the path of signature file
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.file = os.path.abspath(kwargs.get("file"))
        self.pubkey = os.path.abspath(kwargs.get("pubkey"))
        self.signature = os.path.abspath(kwargs.get("signature"))
        self.x509 = crypto.X509()
        self.file_data = None
        self.signature_data = None
        self.pubkey_data = None

    def _load_file(self):
        """
        Loads file to be verified
        """
        with open(self.file, "rb") as f_data:
            self.file_data = f_data.read()

    def _load_signature(self):
        """
        Loads the signature file
        """
        with open(self.signature, "rb") as f_data:
            self.signature_data = f_data.read()

    def _load_public_key(self):
        """
        Loads the public key file
        """
        with open(self.pubkey, encoding="utf-8") as f_data:
            self.pubkey_data = f_data.read()

    def build(self):
        """
        Build verification before verify itself
        """
        self._load_file()
        self._load_signature()
        self._load_public_key()

        # Set public key
        pkey = crypto.load_publickey(crypto.FILETYPE_PEM, self.pubkey_data)
        self.x509.set_pubkey(pkey)

    def verify(self) -> str:
        """
        Use :module:`OpenSSl.crypto` to verify a
        the authenticity of a file with given both
        signature and public key
        """
        msg = ""
        try:
            # Now verify
            # According de documentation found in
            # https://pyopenssl.org/en/stable/api/crypto.html#OpenSSL.crypto.verify
            # it will return :data:`None` if signature is correct
            print("Verifying...")
            crypto.verify(self.x509, self.signature_data, self.file_data, "sha256")
            msg = "Signature verified with success"

        # pylint: disable=broad-exception-caught
        except Exception as exc:
            msg = f"Something wrong is not correct:\n\t{exc}"

        return msg

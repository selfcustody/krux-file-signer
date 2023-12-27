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
signer.py

Export a :class:`Signer` class to be used in `ksigner-cli` and
`ksigner-gui` during `sign` process.
"""
####################
# Standard libraries
####################
import hashlib
import base64

#################
# Local libraries
#################
from utils.constants import KSIGNER_COMPRESSED_PUBKEY_PREPEND
from utils.qr import make_qr_code
from cli.scanner import Scanner


class Signer:
    """
    Signer is the class that manages the `sign` command.

    Kwargs:
    -------
        :param:`file` the file to be signer
        :param:`owner` the owner of file
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.file = kwargs.get("file")
        self.owner = kwargs.get("owner")
        self.scanner = Scanner()

    def sign(self):
        """
        Sign process will:

        (1) Read a file;
        (2) Save in a .sha256.txt file;
        (3) Requires the user loads a xpriv key on his/her device:
            (a) load a 12/24 words key;
            (b) with or without BIP39 password;
        (4) sign a message:
            (a) once loaded the xpriv key, user goes
            to Sign > Message feature on his/her device
            (b) show a qrcode on device;
            (c) this function will generate a qrcode on computer;
            (d) once shown, the user will be prompted to scan it with device;
            (e) once scanned, the device will show some qrcodes:
                (i) the signature as a qrcode;
                (ii) the public key;
            (f) once above qrcodes are scanned, the computer
                will generate a publickey certificate, in a compressed
                or uncompressed format, in name of an owner.
        """

        self._show_warning_messages()
        data = self.hash_file()
        self.save_hash_file(data)
        self._print_qrcode(data)
        sig = self.scan_sig()
        self.save_signature(sig)

    def _show_warning_messages(self):
        """
        Shows warning messages before hash
        """
        print("")
        print("To sign this file with Krux: ")
        print(" (a) load a 12/24 words key with or without password;")
        print(" (b) use the Sign->Message feature;")
        print(" (c) and scan this QR code below.")
        print("")

    def hash_file(self) -> str:
        """
        Creates a hash file before sign
        """
        with open(self.file, "rb") as f_sig:
            _bytes = f_sig.read()
            data = hashlib.sha256(_bytes).hexdigest()
            return data

    def save_hash_file(self, data):
        """
        Save the hash file in sha256sum format
        """
        name = f"{self.file}.sha256sum.txt"

        with open(name, mode="w", encoding="utf-8") as hashfile:
            content = f"{data} {self.file}"
            hashfile.write(content)

    def _print_qrcode(self, data):
        """
        Print QRCode to console
        """
        # Prints the QR code
        __qrcode__ = make_qr_code(data=data)
        print(f"{__qrcode__}\n{data}\n")

    def scan_sig(self):
        """
        Make signature file from scanning qrcode
        """
        return self.scanner.scan_signature()

    def save_signature(self, signature):
        """
        Save the signature data into file
        """
        # Saves a signature
        signature_file = f"{self.file}.sig"

        # encode signature to binary format
        binary_signature = base64.b64decode(signature.encode())

        # Save
        with open(signature_file, "wb") as sig_file:
            sig_file.write(binary_signature)
            msg = f"Signature saved on {signature_file}"
            print(msg)

    def make_pubkey_certificate(self):
        """
        Make public key file from scanning qrcode
        """
        # Scans the public KeyboardInterruptardInterrupt
        pubkey = self.scanner.scan_public_key()
        self.save_pubkey_certificate(pubkey)

    def save_pubkey_certificate(self, pubkey):
        """
        Create and save PEM data to a file
        with filename as owner's name

        Choose if will be compressed or uncompressed
        """
        pub_key_data = f"{KSIGNER_COMPRESSED_PUBKEY_PREPEND}{pubkey}"

        # Convert pubkey data to bytes
        pub_key_data_bytes = bytes.fromhex(pub_key_data)

        # Encoding bytes to base64 format
        pub_key_data_b64 = base64.b64encode(pub_key_data_bytes)

        # Decode bas64 to utf8
        pub_key_data_b64_utf8 = pub_key_data_b64.decode("utf8")

        # Format pubkey
        formated_pubkey = "\n".join(
            [
                "-----BEGIN PUBLIC KEY-----",
                pub_key_data_b64_utf8,
                "-----END PUBLIC KEY-----",
            ]
        )

        # give a filename
        pubkey_name = f"{self.owner}.pem"

        with open(pubkey_name, mode="w", encoding="utf-8") as pb_file:
            pb_file.write(formated_pubkey)
            msg = f"{pubkey_name} saved"
            print(msg)

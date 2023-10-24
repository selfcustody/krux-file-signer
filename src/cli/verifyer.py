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
import subprocess
import logging

#################
# Local libraries
#################
from utils.log import build_logger

class Verifyer:
    """
    Verifyer is the class
    that manages the `verify` verify_openssl_command
    with given :param:`file`, :param:`pubkey` and 
    :param:`signature`
    """

    def __init__(self, **kwargs):
        self.file = kwargs.get("file")
        self.pubkey = kwargs.get("pubkey")
        self.signature = kwargs.get("signature")
        self.loglevel = kwargs.get("loglevel")
        self.log = build_logger(__name__, self.loglevel)

    def make_openssl_command(self) -> str:
        """
        Create the properly openssl command to verify
        """
        
        self.log.debug("Verifyer: Creating openssl command")
        return " ".join(
        [
            f"openssl sha256 <{self.file} -binary",
            "|",
            f"openssl pkeyutl -verify -pubin -inkey {self.pubkey}",
            f"-sigfile {self.signature}",
        ]
    
    )

    def verify(self, command):
        """
        Uses openssl to verify the signature and public key
        """
        try:
            self.log.debug("Verifyer: Running '%s'", command)
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as exc:
            message = "Invalid command"
            numeric_level = getattr(logging, self.loglevel.upper(), None)
            if not numeric_level == logging.NOTSET:
                self.log.error("%s: %s", message, command)
            else:
                raise subprocess.CalledProcessError(message, cmd=command) from exc
            
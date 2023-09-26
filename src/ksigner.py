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
This python script is a tool to create air-gapped signatures of files using Krux.
The script can also convert hex publics exported from Krux to PEM public keys so
signatures can be verified using openssl.

Requirements:
    - opencv, qrcode
    pip install opencv-python qrcode

    - This script also calls a openssl bash command, 
    so it is required to have verification functionality
 """

####################
# Standart libraries
####################
import argparse
import hashlib
import base64

#################
# Local libraries
#################
from constants import *
from logutils import *
from qrutils import *
from videoutils import *
from signandverifyutils import verify
from hashutils import *
from pemutils import *

################
# Command parser
################
parser = argparse.ArgumentParser(prog="ksigner", description=KSIGNER_CLI_DESCRIPTION)

# Verbose messages
parser.add_argument(
    "-V",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="verbose output (default: False)",
    default=False,
)

# Capture pos-processing camera flags
parser.add_argument(
    "-n",
    "--normalize",
    dest="is_normalized",
    action="store_true",
    help="normalizes the image of camera (default: False)",
    default=False,
)

parser.add_argument(
    "-g",
    "--gray-scale",
    dest="is_gray_scale",
    action="store_true",
    help="apply gray-scale filter on camera's image (default: False)",
    default=False,
)

subparsers = parser.add_subparsers(help="sub-command help", dest="command")

# Sign command
signer = subparsers.add_parser("sign", help="sign a file")
signer.add_argument("-f", "--file", dest="file_to_sign", help="path to file to sign")

signer.add_argument(
    "-o",
    "--owner",
    dest="file_owner",
    help="the owner's name of public key certificate, i.e, the .pem file (default: 'pubkey')",
    default="pubkey",
)

signer.add_argument(
    "-u",
    "--uncompressed",
    dest="uncompressed_pub_key",
    action="store_true",
    help="flag to create a uncompreesed public key (default: False)",
)

# Verify command
verifier = subparsers.add_parser("verify", help="verify signature")
verifier.add_argument("-f", "--file", dest="verify_file", help="path to file to verify")
verifier.add_argument(
    "-s", "--sig-file", dest="sig_file", help="path to signature file"
)
verifier.add_argument("-p", "--pub-file", dest="pub_file", help="path to pubkey file")


def on_sign():
    """
    onSign is executed when `sign` command is called
    """
    # If the signergn command was given
    if args.command == "sign" and args.file_to_sign is not None:
        # read file
        data = open_and_hash_file(path=args.file_to_sign, verbose=args.verbose)

        # Saves a hash file
        save_hashed_file(data=data, path=args.file_to_sign, verbose=args.verbose)

        # Shows some message
        verbose_log("To sign this file with Krux: ")
        verbose_log(" (a) load a 24 words key;")
        verbose_log(" (b) use the Sign->Message feature;")
        verbose_log(" (c) and scan this QR code below.")

        # Prints the QR code
        __qrcode__ = make_qr_code(data=data, verbose=args.verbose)
        print(f"\n{__qrcode__}")

        # Scans the signature QR code
        scan_and_save_signature(
            is_normalized=args.is_normalized,
            is_gray_scale=args.is_gray_scale,
            verbose=args.verbose,
        )

        # Scans the public KeyboardInterrupt
        pubkey = scan_public_key(
            is_normalized=args.is_normalized,
            is_gray_scale=args.is_gray_scale,
            verbose=args.verbose,
        )

        # Create PEM data
        # Save PEM data to a file
        # with filename as owner's name
        create_public_key_certificate(
            pubkey=pubkey,
            uncompressed=args.uncompressed_pub_key,
            owner=args.file_owner,
            verbose=args.verbose,
        )


def on_verify():
    """
    onVerify is executed when `verify` command is called
    """
    # Else if the verify command was given
    if (
        args.command == "verify"
        and args.verify_file is not None
        and args.sig_file is not None
        and args.pub_file is not None
    ):
        verify(
            filename=args.verify_file,
            pubkey=args.pub_file,
            sigfile=args.sig_file,
            verbose=args.verbose,
        )
    # If command was not found
    else:
        parser.print_help()


if __name__ == "__main__":
    args = parser.parse_args()
    on_sign()
    on_verify()

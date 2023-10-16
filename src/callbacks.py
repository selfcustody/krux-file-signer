"""
callback.py

Functions to be used during `sign` (on_sign function)
and `verify` (on_verify) operations.
"""

import argparse
from constants import KSIGNER_VERSION
from utils.hash import open_and_hash_file, save_hashed_file
from utils.log import logger
from utils.pem import create_public_key_certificate
from utils.qr import make_qr_code
from utils.signandverify import verify
from utils.video import scan_and_save_signature, scan_public_key


def on_version(parser: argparse.ArgumentParser):
    """
    Show version
    """
    args = parser.parse_args()
    if args.version:
        print(KSIGNER_VERSION)


def on_sign(parser: argparse.ArgumentParser):
    """
    onSign is executed when `sign` command is called:

    (1) Read a file;
    (2) Save in a .sha256.txt file;
    (3) Requires the user loads a xpriv key on his/her
        device:
        (a) load a 12/24 words key;
        (b) with or without BIP39 password;
    (4) sign a message:
        (a) once loaded the xpriv key, user goes
            to Sign > Message feature on his/her device
        (b) show a qrcode on device;
        (c) this function will generate a qrcode on computer;
        (d) once shown, the user will be prompted to scan it with device;
        (d) once scanned, the device will show some qrcodes:
            (i) the signature as a qrcode;
            (ii) the public key;
        (e) once above qrcodes are scanned, the computer
            will generate a publickey certificate, in a compressed
            or uncompressed format, in name of an owner.
    """
    args = parser.parse_args()

    # If the signergn command was given
    if args.command == "sign" and args.file_to_sign is not None:
        # read file

        logger("DEBUG", f"opening {args.file_to_sign}")
        data = open_and_hash_file(path=args.file_to_sign)

        # Saves a hash file
        logger("DEBUG", f"saving {args.file_to_sign}.sha256.txt")
        save_hashed_file(data=data, path=args.file_to_sign)

        # Shows some message
        print("")
        print("To sign this file with Krux: ")
        print(" (a) load a 12/24 words key with or without password;")
        print(" (b) use the Sign->Message feature;")
        print(" (c) and scan this QR code below.")
        print("")

        # Prints the QR code
        logger("DEBUG", f"Adding (data={data})")
        __qrcode__ = make_qr_code(data=data, verbose=args.verbose)
        print(f"{__qrcode__}")

        # Scans the signature QR code
        scan_and_save_signature(
            is_normalized=args.is_normalized,
            is_gray_scale=args.is_gray_scale,
        )

        # Scans the public KeyboardInterruptardInterrupt
        pubkey = scan_public_key(
            is_normalized=args.is_normalized,
            is_gray_scale=args.is_gray_scale,
        )

        # Create PEM data
        # Save PEM data to a file
        # with filename as owner's name
        create_public_key_certificate(
            pubkey=pubkey,
            uncompressed=args.uncompressed_pub_key,
            owner=args.file_owner,
        )


def on_verify(parser: argparse.ArgumentParser):
    """
    onVerify is executed when `verify` command is called

    Args:
        :param parser
            the argument parser instance
    """
    args = parser.parse_args()

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
        )
    # If command was not found
    else:
        parser.print_help()

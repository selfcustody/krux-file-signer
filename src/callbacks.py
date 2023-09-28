"""
callback.py

Functions to be used during `sign` (on_sign function)
and `verify` (on_verify) operations.
"""

import argparse
from constants import KSIGNER_VERSION
from hashutils import open_and_hash_file, save_hashed_file
from logutils import verbose_log
from pemutils import create_public_key_certificate
from qrutils import make_qr_code
from signandverifyutils import verify
from videoutils import scan_and_save_signature, scan_public_key


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

        # Scans the public KeyboardInterruptardInterrupt
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
            verbose=args.verbose,
        )
    # If command was not found
    else:
        parser.print_help()

import argparse
from logutils import *
from hashutils import *
from qrutils import make_qr_code
from videoutils import *
from pemutils import *


def on_sign(parser: argparse.ArgumentParser):
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

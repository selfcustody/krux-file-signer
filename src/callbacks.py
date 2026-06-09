"""
callbacks.py

Functions that run the `sign` and `verify` commands.
"""

import argparse
import logging

from constants import KSIGNER_VERSION
from hashutils import open_and_hash_file, save_hashed_file
from pemutils import create_public_key_certificate
from qrutils import make_qr_code
from signandverifyutils import verify
from videoutils import scan_and_save_signature, scan_public_key

log = logging.getLogger(__name__)


def on_version():
    """Print the version."""
    print(KSIGNER_VERSION)


def on_sign(args: argparse.Namespace):
    """
    Run the `sign` command:

    (1) hash the file given with --file and save it as '<file>.sha256sum.txt';
    (2) print its hash as a QR code to sign with Krux (Sign > Message);
    (3) scan the signature QR code and save it (default '<file>.sig');
    (4) scan the public key QR code and save it as a '<owner>.pem' certificate.
    """
    data = open_and_hash_file(args.file_to_sign)
    save_hashed_file(data, args.file_to_sign)

    log.info("To sign this file with Krux: ")
    log.info(" (a) load a 24 words key;")
    log.info(" (b) use the Sign->Message feature;")
    log.info(" (c) and scan this QR code below.")
    print(f"\n{make_qr_code(data)}")

    # Scan the signature; default the output to '<file_to_sign>.sig'
    signature_file = args.sig_file or f"{args.file_to_sign}.sig"
    scan_and_save_signature(
        signature_file,
        is_normalized=args.is_normalized,
        is_gray_scale=args.is_gray_scale,
    )

    # Scan the public key and save it as a PEM certificate named after the owner
    pubkey = scan_public_key(
        is_normalized=args.is_normalized, is_gray_scale=args.is_gray_scale
    )
    create_public_key_certificate(
        pubkey, uncompressed=args.uncompressed_pub_key, owner=args.file_owner
    )


def on_verify(args: argparse.Namespace):
    """Run the `verify` command: check a file against its signature and public key."""
    verify(filename=args.verify_file, pubkey=args.pub_file, sigfile=args.sig_file)

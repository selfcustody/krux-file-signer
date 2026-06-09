"""
signandverifyutils.py

Use openssl as a wrapper to verify signatures.

TODO: replace with pyca/cryptography or pyOpenSSL.
"""

import logging
import subprocess

log = logging.getLogger(__name__)


def verify_openssl_command(file: str, pubkey: str, signature: str) -> str:
    """Build the openssl command that verifies `file` against `signature` with `pubkey`."""
    return " ".join(
        [
            f"openssl sha256 <{file} -binary",
            "|",
            f"openssl pkeyutl -verify -pubin -inkey {pubkey}",
            f"-sigfile {signature}",
        ]
    )


def verify(filename: str, pubkey: str, sigfile: str):
    """Verify `filename` against `sigfile` and `pubkey` using openssl."""
    log.info("Verifying signature:")
    command = verify_openssl_command(file=filename, pubkey=pubkey, signature=sigfile)
    log.debug("%s", command)
    subprocess.run(command, check=True, shell=True)

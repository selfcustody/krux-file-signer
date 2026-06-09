"""
pemutils.py

Create public key certificates (.pem files) in compressed or
uncompressed format.

@see src/constants.py::KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND
@see src/constants.py::KSIGNER_COMPRESSED_PUBKEY_PREPEND
"""

import base64

from constants import KSIGNER_COMPRESSED_PUBKEY_PREPEND
from constants import KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND
from logutils import verbose_log


def create_public_key_certificate(
    pubkey: str,
    uncompressed: bool = False,
    owner: str = "pubkey",
    verbose: bool = False,
):
    """
    Build a PEM public key certificate from the hex `pubkey` and save it
    as '<owner>.pem'.
    """
    prepend = (
        KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND
        if uncompressed
        else KSIGNER_COMPRESSED_PUBKEY_PREPEND
    )
    if verbose:
        verbose_log(
            f"Creating {'uncompressed' if uncompressed else 'compressed'} "
            "public key certificate"
        )

    # prepend + pubkey is a DER (binary) key; a PEM body is just its base64.
    der_bytes = bytes.fromhex(f"{prepend}{pubkey}")
    pem_body = base64.b64encode(der_bytes).decode("ascii")
    pem = "\n".join(
        ["-----BEGIN PUBLIC KEY-----", pem_body, "-----END PUBLIC KEY-----"]
    )
    if verbose:
        verbose_log(pem)

    pem_file = f"{owner}.pem"
    if verbose:
        verbose_log(f"Saving public key file: {pem_file}")

    with open(pem_file, mode="w", encoding="utf-8") as file:
        file.write(pem)

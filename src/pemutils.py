"""
pemutils.py

Create public key certificates (.pem files) in compressed or
uncompressed format.

@see src/constants.py::KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND
@see src/constants.py::KSIGNER_COMPRESSED_PUBKEY_PREPEND
"""

import base64
import logging

from constants import KSIGNER_COMPRESSED_PUBKEY_PREPEND
from constants import KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND

log = logging.getLogger(__name__)


def create_public_key_certificate(
    pubkey: str, uncompressed: bool = False, path: str = "pubkey.pem"
):
    """
    Build a PEM public key certificate from the hex `pubkey` and save it to `path`.
    """
    prepend = (
        KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND
        if uncompressed
        else KSIGNER_COMPRESSED_PUBKEY_PREPEND
    )
    log.debug(
        "Creating %s public key certificate",
        "uncompressed" if uncompressed else "compressed",
    )

    # prepend + pubkey is a DER (binary) key; a PEM body is just its base64.
    der_bytes = bytes.fromhex(f"{prepend}{pubkey}")
    pem_body = base64.b64encode(der_bytes).decode("ascii")
    pem = "\n".join(
        ["-----BEGIN PUBLIC KEY-----", pem_body, "-----END PUBLIC KEY-----"]
    )
    log.debug("%s", pem)

    log.debug("Saving public key file: %s", path)
    with open(path, mode="w", encoding="utf-8") as file:
        file.write(pem)

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
from constants import KSIGNER_SECP256K1_P

log = logging.getLogger(__name__)


def decompress_pubkey(compressed: bytes) -> bytes:
    """
    Recover 65-byte uncompressed SEC point from a 33-byte compressed key.
    """
    # Krux only a compressed public key, so we must rebuild y from secp256k1 equation
    if len(compressed) != 33 or compressed[0] not in (0x02, 0x03):
        raise ValueError("not a compressed SEC public key (need 33 bytes, 0x02/0x03)")

    prefix = compressed[0]
    x = int.from_bytes(compressed[1:], "big")
    y_2 = (pow(x, 3, KSIGNER_SECP256K1_P) + 7) % KSIGNER_SECP256K1_P
    y = pow(y_2, (KSIGNER_SECP256K1_P + 1) // 4, KSIGNER_SECP256K1_P)
    if (y * y) % KSIGNER_SECP256K1_P != y_2:
        raise ValueError("invalid compressed pubkey")
    if (y & 1) != (prefix & 1):
        y = KSIGNER_SECP256K1_P - y

    return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")


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

    key_bytes = bytes.fromhex(pubkey)
    if uncompressed and len(key_bytes) == 33:
        key_bytes = decompress_pubkey(key_bytes)

    der_bytes = bytes.fromhex(prepend) + key_bytes
    pem_body = base64.b64encode(der_bytes).decode("ascii")
    pem = "\n".join(
        ["-----BEGIN PUBLIC KEY-----", pem_body, "-----END PUBLIC KEY-----"]
    )
    log.debug("%s", pem)

    log.debug("Saving public key file: %s", path)
    with open(path, mode="w", encoding="utf-8") as file:
        file.write(pem)

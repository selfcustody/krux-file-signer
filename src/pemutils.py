from constants import *
from logutils import *


def create_public_key_certificate(**kwargs):
    """
    Create public key certifficate file (.pem)

    Kwargs:
        :param pubkey
            The generated public key
        :param uncompressed
            Flag to create a uncompressed public key certificate
        :param owner
            Owner of public key certificate
        :is_normalized
            Apply or not normalization on image
        :is_gray_scale
            Apply or not gray scale on image
        :param verbose
            Apply verbose or not
    """
    hex_pubkey = kwargs.get("pubkey")
    uncompressed = kwargs.get("uncompressed")
    owner = kwargs.get("owner")
    verbose = kwargs.get("verbose")

    # Choose if will be compressed or uncompressed
    if uncompressed:
        if verbose:
            verbose_log("Creating uncompressed public key certificate")
        __public_key_data__ = f"{KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND}{hex_pubkey}"

    else:
        if verbose:
            verbose_log("Creating compressed public key certificate")
        __public_key_data__ = f"{KSIGNER_COMPRESSED_PUBKEY_PREPEND}{hex_pubkey}"

    # Convert pubkey data to bytes
    __public_key_data_bytes__ = bytes.fromhex(__public_key_data__)
    if verbose:
        verbose_log(f"pubkey bytes: {__public_key_data_bytes__}")

    # Decode to utf8
    __public_key_data_utf8__ = __public_key_data_bytes__.decode("utf-8")
    if verbose:
        verbose_log(f"pubkey utf8: {__public_key_data_utf8__}")

    # Encode to formated base64
    __pem_pub_key__ = "\n".join(
        [
            "-----BEGIN PUBLIC KEY-----",
            base64.b64encode(__public_key_data_utf8__),
            "-----END PUBLIC KEY-----",
        ]
    )

    if verbose:
        verbose_log(__pem_pub_key__)

    __pem_key_file__ = f"{owner}.pem"
    if verbose:
        verbose_log(f"Saving public key file: {__pem_key_file__}")

    with open(file=__pem_key_file__, mode="w", encoding="utf-8") as pem_file:
        pem_file.write(__pem_pub_key__)

"""
pemutils.py

Utility for create public key certificates (aka .pem files),
in uncompressed or compressed formats

@see src/constants.py::KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND
@see src/constants.py::KSIGNER_COMPRESSED_PUBKEY_PREPEND
"""

####################
# Stardard libraries
####################
import base64

#################
# Local libraries
#################
from constants import KSIGNER_COMPRESSED_PUBKEY_PREPEND
from constants import KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND


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
        :issubclass_gray_scale
            Apply or not gray scale on image
        :param verbose
            Apply verbose or not
    """
    hex_pubkey = kwargs.get("pubkey")
    uncompressed = kwargs.get("uncompressed")
    owner = kwargs.get("owner")


"""
hashutils.py

Utility for create and save
files in sha256sum format
"""
####################
# Standard libraries
####################
import hashlib

#################
# Local libraries
#################
from logutils import verbose_log


def open_and_hash_file(**kwargs) -> str:
    """ "
    Read file from --file argument on `sign` command and return its hash

    Kwargs:
        :param path
            The path of file to be hashed
        :param verbose
            Apply verbose or not
    """
    __filename__ = kwargs.get("path")
    verbose = kwargs.get("verbose")

    try:
        with open(__filename__, "rb") as f_to_be_sig:
            _bytes = f_to_be_sig.read()  # read file as bytes

            if verbose:
                verbose_log('INFO', f"Read bytes: {_bytes}")

            __readable_hash__ = hashlib.sha256(_bytes).hexdigest()

            # Prints the hash of the file
            if verbose:
                verbose_log('INFO', f"Hash of {__filename__}: {__readable_hash__}")

            return __readable_hash__
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Unable to read target file: {__filename__}") from exc


def save_hashed_file(**kwargs):
    """
    Appends '.sha256.txt' to `**kwargs<path>`
    and creates its hashed file with `data` content

    Kwargs:
        :param data
            The data to hashed
        :param path
            The <path>.sha256.txt
        :param verbose
            Apply verbose or not
    """
    __data__ = kwargs.get("data")
    __path__ = kwargs.get("path")
    verbose = kwargs.get("verbose")

    __hash_file__ = f"{__path__}.sha256sum.txt"

    if verbose:
        verbose_log(f"Saving a hash file: {__hash_file__}")

    with open(__hash_file__, mode="w", encoding="utf-8") as hash_file:
        hash_file.write(f"{__data__} {__hash_file__}")

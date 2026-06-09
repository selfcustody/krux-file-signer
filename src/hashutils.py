"""
hashutils.py

Utilities to create and save files in sha256sum format.
"""

import hashlib
import logging

log = logging.getLogger(__name__)


def open_and_hash_file(path: str) -> str:
    """
    Read the file at `path` (the `sign` command's --file) and return its
    sha256 hex digest.
    """
    try:
        with open(path, "rb") as file_to_sign:
            file_bytes = file_to_sign.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Unable to read target file: {path}") from exc

    log.debug("Read bytes: %s", file_bytes)
    readable_hash = hashlib.sha256(file_bytes).hexdigest()
    log.debug("Hash of %s: %s", path, readable_hash)
    return readable_hash


def save_hashed_file(data: str, path: str):
    """Write `data` (a hash) to '<path>.sha256sum.txt' in sha256sum format."""
    hash_file = f"{path}.sha256sum.txt"
    log.debug("Saving a hash file: %s", hash_file)
    with open(hash_file, mode="w", encoding="utf-8") as file:
        file.write(f"{data}  {path}")

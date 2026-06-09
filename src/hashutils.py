"""
hashutils.py

Utilities to create and save files in sha256sum format.
"""

import hashlib

from logutils import verbose_log


def open_and_hash_file(path: str, verbose: bool = False) -> str:
    """
    Read the file at `path` (the `sign` command's --file) and return its
    sha256 hex digest.
    """
    try:
        with open(path, "rb") as file_to_sign:
            file_bytes = file_to_sign.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Unable to read target file: {path}") from exc

    if verbose:
        verbose_log(f"Read bytes: {file_bytes}")

    readable_hash = hashlib.sha256(file_bytes).hexdigest()
    if verbose:
        verbose_log(f"Hash of {path}: {readable_hash}")

    return readable_hash


def save_hashed_file(data: str, path: str, verbose: bool = False):
    """
    Write `data` (a hash) to '<path>.sha256sum.txt' in sha256sum format.
    """
    hash_file = f"{path}.sha256sum.txt"
    if verbose:
        verbose_log(f"Saving a hash file: {hash_file}")

    with open(hash_file, mode="w", encoding="utf-8") as file:
        file.write(f"{data}  {path}")

"""
hashutils.py

Utility for create and save
files in sha256sum format
"""
####################
# Standard libraries
####################
import logging
import hashlib

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


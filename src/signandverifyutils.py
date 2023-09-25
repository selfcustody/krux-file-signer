####################
# Standart libraries
####################
import subprocess

#################
# Local libraries
#################
from logutils import *

def verifyOpensslCommand(**kwargs) -> str:
    """
    Create the properly openssl command 
    to verify, for given:
    
    - A `signature` to verify the `file` agains `pubkey`

    Kwargs:
        :param file
            The `file` to be verified
        :param pubkey
            The `pubkey` file path to certifacate
        :param signature
            The `signature` to verify the `file`
            against its `signature`
    """
    file2verify = kwargs.get('file')
    pubkey = kwargs.get('pubkey')
    sig = kwargs.get('signature')

    return " ".join(
        [
            f"openssl sha256 <{file2verify} -binary",
            "|",
            f"openssl pkeyutl -verify -pubin -inkey {pubkey}",
            f"-sigfile {sig}",
        ]
    )

def verify(**kwargs):
    """
    Uses openssl to verify the signature and public key

    Kwargs:
        :param filename
            The path of file to be veryfied
        :param pubkey
            The path of file that be used to verify `filename`
        :param sigfile
            The path of signature file that will be used to verify `filename`
        :param verbose
            Apply verbose or no

    """
    verbose_log("Verifying signature:")

    file2verify = kwargs.get("filename")
    pubkey_file = kwargs.get("pubkey")
    sig_file = kwargs.get("sigfile")
    verbose = kwargs.get("verbose")

    try:
        __command__ = verifyOpensslCommand(
            file=file2verify,
            pubkey=pubkey_file,
            signature=sig_file     
        )
        if verbose:
            verbose_log(__command__)
        subprocess.run(__command__, check=True, shell=True)
    except subprocess.CalledProcessError as __exc__:
        raise subprocess.CalledProcessError(
            "Invalid command", cmd=__command__
        ) from __exc__

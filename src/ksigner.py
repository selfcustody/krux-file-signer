# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This python script is a tool to create air-gapped signatures of files using Krux.
The script can also convert hex publics exported from Krux to PEM public keys so
signatures can be verified using openssl.

Requirements:
    - opencv, qrcode
    pip install opencv-python qrcode

    - This script also calls a openssl bash command, 
    so it is required to have verification functionality
 """

####################
# Standart libraries
####################
import argparse
import hashlib
import subprocess
import base64
import time
from io import StringIO

#######################
# Thrid party libraries
#######################
import cv2
from qrcode import QRCode

# PUBKEY pre-String:
# ASN.1 STRUCTURE FOR PUBKEY (uncompressed and compressed):
#   30  <-- declares the start of an ASN.1 sequence
#   56  <-- length of following sequence (dez 86)
#   30  <-- length declaration is following
#   10  <-- length of integer in bytes (dez 16)
#   06  <-- declares the start of an "octet string"
#   07  <-- length of integer in bytes (dez 7)
#   2a 86 48 ce 3d 02 01 <-- Object Identifier: 1.2.840.10045.2.1
#                            = ecPublicKey, ANSI X9.62 public key type
#   06  <-- declares the start of an "octet string"
#   05  <-- length of integer in bytes (dez 5)
#   2b 81 04 00 0a <-- Object Identifier: 1.3.132.0.10
#                      = secp256k1, SECG (Certicom) named eliptic curve
#   03  <-- declares the start of an "octet string"
#   42  <-- length of bit string to follow (66 bytes)
#   00  <-- Start pubkey??
#
# example for setup of 'pre' public key strings above:
#   openssl ecparam -name secp256k1 -genkey -out ec-priv.pem
#   openssl ec -in ec-priv.pem -pubout -out ec-pub.pem
#   openssl ec -in ec-priv.pem -pubout -conv_form compressed -out ec-pub_c.pem
#   cat ec-pub.pem
#   cat ec-pub_c.pem
#   echo "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEAd+5gxspjAfO7HA8qq0/    \
#         7NbHrtTA3z9QNeI5TZ8v0l1pMJ1+mkg3d6zZVUXzMQZ/Y41iID+JAx/ \
#         sQrY+wqVU/g==" | base64 -D - > ec-pub_uc.hex
#   echo "MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgACAd+5gxspjAfO7HA8qq0/7Nb \
#         HrtTA3z9QNeI5TZ8v0l0=" | base64 -D - > ec-pub_c.hex
#   hexdump -C ec-pub_uc.hex
#   hexdump -C ec-pub_c.hex
#
# @see https://github.com/selfcustody/krux/blob/a63dc4ae917afc7ecd7773e6a4b13c23ea2da4d3/krux#L139
# @see https://github.com/pebwindkraft/trx_cl_suite/blob/master/tcls_key2pem.sh#L134
UNCOMPRESSED_PUBKEY_PREPEND = "3056301006072A8648CE3D020106052B8104000A034200"
COMPRESSED_PUBKEY_PREPEND = "3036301006072A8648CE3D020106052B8104000A032200"

DESCRIPTION = "".join(
    [
        "This python script is a tool to create air-gapped signatures of files using Krux. ",
        "The script can also convert hex publics exported from Krux to PEM public keys so ",
        "signatures can be verified using openssl.",
    ]
)
parser = argparse.ArgumentParser(prog="ksigner", description=DESCRIPTION)

# Verbose messages
parser.add_argument(
    "--verbose",
    dest="verbose",
    action="store_true",
    help="verbose output (default: False)",
    default=False,
)

# Capture pos-processing camera flags
parser.add_argument(
    "-n",
    "--normalize",
    dest="is_normalized",
    action="store_true",
    help="normalizes the image of camera (default: False)",
    default=False,
)

parser.add_argument(
    "-g",
    "--gray-scale",
    dest="is_gray_scale",
    action="store_true",
    help="apply gray-scale filter on camera's image (default: False)",
    default=False,
)

subparsers = parser.add_subparsers(help="sub-command help", dest="command")

# Sign command
signer = subparsers.add_parser("sign", help="sign a file")
signer.add_argument("-f", "--file", dest="file_to_sign", help="path to file to sign")

signer.add_argument(
    "-o",
    "--owner",
    dest="file_owner",
    help="the owner's name of public key certificate, i.e, the .pem file (default: 'pubkey')",
    default="pubkey",
)

signer.add_argument(
    "-u",
    "--uncompressed",
    dest="uncompressed_pub_key",
    action="store_true",
    help="flag to create a uncompreesed public key (default: False)",
)

# Verify command
verifier = subparsers.add_parser("verify", help="verify signature")
verifier.add_argument("-f", "--file", dest="verify_file", help="path to file to verify")

verifier.add_argument(
    "-s", "--sig-file", dest="sig_file", help="path to signature file"
)

verifier.add_argument("-p", "--pub-file", dest="pub_file", help="path to pubkey file")


############
# FUNCTIONS
############
def now() -> str:
    """Return some formated time"""
    return time.strftime("%X %x %Z")


def verbose_log(v_data):
    """Prints verbose data preceded by current time"""
    print(f"[{now()}] {v_data}")


def make_qr_code(**kwargs) -> str:
    """
    Builds the ascii data to QR code

    Kwargs:
        :param data
            The data to be encoded in qrcode
        :param verbose
            Apply verbose or not
    """
    qr_data = kwargs.get("data")
    verbose = kwargs.get("verbose")

    qr_code = QRCode()

    if verbose:
        verbose_log(f"Adding (data={qr_data})")

    qr_code.add_data(qr_data)
    qr_string = StringIO()
    qr_code.print_ascii(out=qr_string, invert=True)
    return qr_string.getvalue()


def make_qr_code_image(**kwargs) -> str:
    """
    Creates a QR code image

    Kwargs:
        :param data
            The data to be encoded in qrcode
        :param verbose
            Apply verbose or not
    """
    qr_data = kwargs.get("data")
    verbose = kwargs.get("verbose")

    qr_code = QRCode()

    if verbose:
        verbose_log(f"Adding (data={qr_data})")

    qr_code.add_data(qr_data)
    qr_image = qr_code.make_image()
    return qr_image


def normalization_transform(**kwargs):
    """ "
    Apply Gray scale on frames

    Kwargs
        :param frame
            The frame which will be applyed the transformation
        :param verbose
            Apply verbose messages
    """
    frame = kwargs.get("frame")
    verbose = kwargs.get("verbose")

    # Cameras have different configurations
    # and behaviours, so try apply some normalization
    # @see https://stackoverflow.com/questions/61016954/
    # controlling-contrast-and-brightness-of-video-stream-in-opencv-and-python
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

    # Verbose some data
    if verbose:
        verbose_log(f"normalized (frame={frame})")


def gray_transform(**kwargs):
    """ "
    Apply Gray scale on frames

    Kwargs
        :param ret
        :param frame
            The frame which will be applyed the transformation
        :param verbose
            Apply verbose messages
    """
    frame = kwargs.get("frame")
    verbose = kwargs.get("verbose")

    # Convert frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # verbose_loge some data
    if verbose:
        verbose_log(f"gray scale (frame={frame})")


def scan(**kwargs) -> str:
    """
    Opens a scan window and uses cv2 to detect
    and decode a QR code, returning its data.
    Can be applyed some normalization
    or gray scale

    Kwargs:
        :is_normalized
            Apply some normalization
        :is_gray_scale
            Apply some gray scale
        :param verbose
            Apply or not verify
    """
    verbose = kwargs.get("versbose")
    is_normalized = kwargs.get("is_normalized")
    is_gray_scale = kwargs.get("is_gray_scale")

    verbose_log("Opening camera")
    vid = cv2.VideoCapture(0)

    verbose_log("Starting detection")
    detector = cv2.QRCodeDetector()

    qr_data = None
    while True:
        # Capture the video frame by frame
        # use some dummy vars (__+[a-zA-Z0-9]*?$)
        # to avoid the W0612 'Unused variable' pylint message
        _ret, frame = vid.read()

        # Apply some normalization if wanted
        if is_normalized:
            normalization_transform(frame=frame, verbose=verbose)

        # Apply gray scale if wanted
        if is_gray_scale:
            gray_transform(frame=frame)

        # Detect qrcode
        qr_data, _bbox, _straight_qrcode = detector.detectAndDecode(frame)

        # Verbose some data
        if verbose:
            verbose_log(f"reading (qr_data={qr_data})")
            verbose_log(f"reading (_bbox={_bbox}")
            verbose_log(f"reading (_straight_qrcode={_straight_qrcode})")

        # Verify null data
        if verbose:
            verbose_log(f"len(qr_data) = {len(qr_data)}")

        if len(qr_data) > 0:
            break

        # Display the resulting frame
        if verbose:
            verbose_log(f"Showing (frame={frame})")

        # Show image
        cv2.imshow("frame", frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if verbose:
                verbose_log("quiting QRCode detection...")
            break

    # After the loop release the cap object
    if verbose:
        verbose_log("Releasing video...")

    vid.release()

    # Destroy all the windows
    if verbose:
        verbose_log("Destroying all ksigner windows...")

    cv2.destroyAllWindows()

    return qr_data


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
    pub_key_file = kwargs.get("pubkey")
    sig_file = kwargs.get("sigfile")
    verbose = kwargs.get("verbose")

    __command__ = " ".join(
        [
            f"openssl sha256 <{file2verify} -binary",
            "|",
            f"openssl pkeyutl -verify -pubin -inkey {pub_key_file}",
            f"-sigfile {sig_file}",
        ]
    )
    try:
        if verbose:
            print(__command__)
        subprocess.run(__command__, check=True, shell=True)
    except subprocess.CalledProcessError as __exc__:
        raise subprocess.CalledProcessError(
            "Invalid command", cmd=__command__
        ) from __exc__


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
                verbose_log(f"Read bytes: {_bytes}")

            __readable_hash__ = hashlib.sha256(_bytes).hexdigest()

            # Prints the hash of the file
            if verbose:
                verbose_log(f"Hash of {__filename__}: {__readable_hash__}")

            return __readable_hash__
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Unable to read target file: {args.file_to_sign}"
        ) from exc


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


def scan_and_save_signature(**kwargs):
    """
    Scan with camera the generated signatue

    Kwargs:
        :is_normalized
            Apply normalization on video
        :is_gray_scale
            Apply some gray scale on video
        :param verbose
    """
    is_normalized = kwargs.get("is_normalized")
    is_gray_scale = kwargs.get("is_gray_scale")
    verbose = kwargs.get("verbose")

    _ = input(f"[{now()}] Press enter to scan signature")
    signature = scan(
        is_normalized=is_normalized, is_gray_scale=is_gray_scale, verbose=verbose
    )

    # Encode data
    binary_signature = base64.b64decode(signature.encode())
    if verbose:
        verbose_log(f"Signature: {binary_signature}")

    # Saves a signature
    signature_file = f"{args.file_to_sign}.sig"
    verbose_log(f"Saving a signature file: {signature_file}")
    with open(signature_file, "wb") as sig_file:
        sig_file.write(binary_signature)


def scan_public_key(**kwargs) -> str:
    """
    Scan with camera the generated public key

    Kwargs:
        :is_normalized
            Apply or not normalization on image
        :is_gray_scale
            Apply or not gray scale on image
        :param verbose
    """
    is_normalized = kwargs.get("is_normalized")
    is_gray_scale = kwargs.get("is_gray_scale")
    verbose = kwargs.get("verbose")

    _ = input(f"[{now()}] Press enter to scan public key")
    public_key = scan(
        is_normalized=is_normalized, is_gray_scale=is_gray_scale, verbose=verbose
    )

    if verbose:
        verbose_log(f"Public key: {public_key}")

    return public_key


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
        __public_key_data__ = f"{UNCOMPRESSED_PUBKEY_PREPEND}{hex_pubkey}"

    else:
        if verbose:
            verbose_log("Creating compressed public key certificate")
        __public_key_data__ = f"{COMPRESSED_PUBKEY_PREPEND}{hex_pubkey}"

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


def on_sign():
    """
    onSign is executed when `sign` command is called
    """
    # If the signergn command was given
    if args.command == "sign" and args.file_to_sign is not None:
        # read file
        data = open_and_hash_file(path=args.file_to_sign, verbose=args.verbose)

        # Saves a hash file
        save_hashed_file(data=data, path=args.file_to_sign, verbose=args.verbose)

        # Shows some message
        verbose_log("To sign this file with Krux: ")
        verbose_log(" (a) load a 24 words key;")
        verbose_log(" (b) use the Sign->Message feature;")
        verbose_log(" (c) and scan this QR code below.")

        # Prints the QR code
        __qrcode__ = make_qr_code(data=data, verbose=args.verbose)
        print(f"\n{__qrcode__}")

        # Scans the signature QR code
        scan_and_save_signature(
            is_normalized=args.is_normalized,
            is_gray_scale=args.is_gray_scale,
            verbose=args.verbose,
        )

        # Scans the public KeyboardInterrupt
        pubkey = scan_public_key(
            is_normalized=args.is_normalized,
            is_gray_scale=args.is_gray_scale,
            verbose=args.verbose,
        )

        # Create PEM data
        # Save PEM data to a file
        # with filename as owner's name
        create_public_key_certificate(
            pubkey=pubkey,
            uncompressed=args.uncompressed_pub_key,
            owner=args.file_owner,
            verbose=args.verbose,
        )


def on_verify():
    """
    onVerify is executed when `verify` command is called
    """
    # Else if the verify command was given
    if (
        args.command == "verify"
        and args.verify_file is not None
        and args.sig_file is not None
        and args.pub_file is not None
    ):
        verify(
            filename=args.verify_file,
            pubkey=args.pub_file,
            sigfile=args.sig_file,
            verbose=args.verbose,
        )
    # If command was not found
    else:
        parser.print_help()


if __name__ == "__main__":
    args = parser.parse_args()
    on_sign()
    on_verify()

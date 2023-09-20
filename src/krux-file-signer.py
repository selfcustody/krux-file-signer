"""
This python script is aimed to help and teach how Krux can be used to sign
files and create PEM public keys so openssl can be used to verify

Requirements:
    - opencv, qrcode
    pip install opencv-python qrcode

    - This script also calls a openssl bash command, 
    so it is required to have verification functionality
 """
import argparse
import hashlib
import subprocess
import base64
from io import StringIO
import cv2
from qrcode import QRCode

parser = argparse.ArgumentParser(
    prog="krux_file_signer",
    description="This python script is aimed to help"
    + " and teach how Krux can be used to sign files"
    + " and create PEM public keys so openssl can be"
    + " used to verify",
)

subparsers = parser.add_subparsers(help="sub-command help", dest="command")
signer = subparsers.add_parser("sign", help="sign a file")
signer.add_argument("--file", dest="file_to_sign", help="path to file to sign")

verifier = subparsers.add_parser("verify", help="verify signature")
verifier.add_argument("--file", dest="verify_file", help="path to file to verify")
verifier.add_argument("--sig-file", dest="sig_file", help="path to signature file")
verifier.add_argument("--pub-file", dest="pub_file", help="path to pubkey file")


def print_qr_code(data):
    """Prints ascii QR code"""
    qr_code = QRCode()
    qr_code.add_data(data)
    qr_string = StringIO()
    qr_code.print_ascii(out=qr_string, invert=True)
    print(qr_string.getvalue())


def scan():
    """Opens a scan window and uses cv2 to detect and decode a QR code, returning its data"""
    vid = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    qr_data = None
    while True:
        # Capture the video frame by frame
        # use some dummy vars (__+[a-zA-Z0-9]*?$)
        # to avoid the W0612 'Unused variable' pylint message
        _ret, frame = vid.read()
        qr_data, _bbox, _straight_qrcode = detector.detectAndDecode(frame)

        # Verify null data
        if len(qr_data) > 0:
            break

        # Display the resulting frame
        cv2.imshow("frame", frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # After the loop release the cap object
    vid.release()

    # Destroy all the windows
    cv2.destroyAllWindows()

    return qr_data


def verify(file2verify, pub_key_file, sig_file):
    """Uses openssl to verify the signature and public key"""
    print("Verifying signature:")

    __command__ = " ".join(
        [
            f"openssl sha256 {file2verify} -binary",
            "|",
            f"openssl pkeyutl -verify -pubin -inkey {pub_key_file}",
            f"-sigfile {sig_file}",
        ]
    )
    try:
        subprocess.run(__command__, check=True, shell=True)
    except subprocess.CalledProcessError as __exc__:
        raise subprocess.CalledProcessError(
            "Invalid command", cmd=__command__
        ) from __exc__


args = parser.parse_args()

# If the sign command was given
if args.command == "sign" and args.file_to_sign is not None:
    file_name = args.file_to_sign
    try:
        with open(file_name, "rb") as f:
            _bytes = f.read()  # read file as bytes
            __readable_hash__ = hashlib.sha256(_bytes).hexdigest()
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Unable to read target file: {args.file_to_sign}"
        ) from exc

    # Prints the hash of the file
    print(f"Hash of {file_name}:")
    print(__readable_hash__ + "\n")

    # Saves a hash file
    __hash_file__ = file_name + ".sha256sum.txt"
    print("Saving a hash file:", __hash_file__)
    with open(__hash_file__, mode="w", encoding="utf-8") as f:
        f.write(__readable_hash__)

    print("To sign this file with Krux: ")
    print(" (a) load a 24 words key;")
    print(" (b) use the Sign->Message feature;")
    print(" (c) and scan this QR code below.")

    # Prints the QR code
    print_qr_code(__readable_hash__)

    # Scans the signature QR code
    _ = input("Press enter to scan signature")
    signature = scan()
    binary_signature = base64.b64decode(signature.encode())
    # Prints signature
    print("Signature:", signature)
    # Saves a signature file
    signature_file = file_name + ".sig"
    print("Saving a signature file:", signature_file)
    with open(signature_file, "wb") as f:
        f.write(binary_signature)

    # Scans the public key
    _ = input("Press enter to scan public key")
    public_key = scan()

    # Prints public key
    print("Public key:", public_key)

    # Saves a PEM public key file
    __public_key_data__ = f"3036301006072A8648CE3D020106052B8104000A032200{public_key}"
    public_key_base64 = base64.b64encode(bytes.fromhex(__public_key_data__)).decode(
        "utf-8"
    )
    __pem_pub_key__ = "\n".join(
        ["-----BEGIN PUBLIC KEY-----", public_key_base64, "-----END PUBLIC KEY-----"]
    )
    __pub_key_file__ = "public_key.PEM"
    print("Saving public key file:", __pub_key_file__)
    with open(__pub_key_file__, mode="w", encoding="utf-8") as f:
        f.write(__pem_pub_key__)

    # Verify signature
    verify(file_name, __pub_key_file__, signature_file)

# Else if the verify command was given
elif (
    args.command == "verify"
    and args.verify_file is not None
    and args.sig_file is not None
    and args.pub_file is not None
):
    verify(args.verify_file, args.pub_file, args.sig_file)
# If command was not found
else:
    parser.print_help()

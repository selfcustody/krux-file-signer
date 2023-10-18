"""
signer.py

Functions to be used during `sign` (on_sign function)
and `verify` (on_verify) operations.
"""

from utils.hash import open_and_hash_file
from utils.pem import create_public_key_certificate
from utils.qr import make_qr_code
from utils.signandverify import verify_file
from utils.video import scan_signature, scan_public_key


class Signer:
    """
    Signer is the class
    that manages the `sign` command

    Workflow:
        
    (1) Read a file;
    (2) Save in a .sha256.txt file;
    (3) Requires the user loads a xpriv key on his/her device:
        (a) load a 12/24 words key;
        (b) with or without BIP39 password;
    (4) sign a message:
        (a) once loaded the xpriv key, user goes
            to Sign > Message feature on his/her device
        (b) show a qrcode on device;
        (c) this function will generate a qrcode on computer;
        (d) once shown, the user will be prompted to scan it with device;
        (e) once scanned, the device will show some qrcodes:
            (i) the signature as a qrcode;
            (ii) the public key;
        (f) once above qrcodes are scanned, the computer
            will generate a publickey certificate, in a compressed
            or uncompressed format, in name of an owner.
    """
    
    def __init__(self, **kwargs):
        self.file = kwargs.get('file')
        self.owner = kwargs.get('owner')
        self.uncompressed = kwargs.get('uncompressed')

    def sign(self):
        self._show_warning_messages()
        data = self._hash_file()
        self._save_hash_file(data)
        self._print_qrcode(data)
        self._make_sig()

    def _show_warning_messages(self):
        """
        Shows warning messages before hash
        """
        logger("DEBUG", "cli:sign", "Showing warning messages to sign")        
        
        # Shows some message
        print("")
        print("To sign this file with Krux: ")
        print(" (a) load a 12/24 words key with or without password;")
        print(" (b) use the Sign->Message feature;")
        print(" (c) and scan this QR code below.")
        print("")

    def _hash_file(self) -> str:
        """
        Creates a hash file before sign
        """ 
        logger("DEBUG", "cli:sign", f"Opening {self.file}")
        return open_and_hash_file(path=self.file)

    def _save_hash_file(self, data): 
        """
        Save the hash file in sha256sum format
        """
        # Saves a hash file
        logger("INFO", "cli:sign", f"Saving {self.file}.sha256.txt")
        __hash_file__ = f"{self.file}.sha256sum.txt" 
        with open(__hash_file__, mode="w", encoding="utf-8") as hash_file:
            hash_file.write(f"{data} {file_to_sign}")

    def _print_qrcode(self, data):
        """
        Print QRCode to console
        """
        # Prints the QR code
        logger("DEBUG", "cli:sign", f"Adding (data={data})")
        __qrcode__ = make_qr_code(data=data, verbose=args.verbose)
        print(f"{__qrcode__}")


    def _make_sig(self):
        """
        Do signature, public key and public key certificates
        """
        # Scans the signature QR code
        logger("INFO", "cli:sign", "Creating signature")
        signature = scan_signature()
        
        # Saves a signature
        signature_file = f"{self.file}.sig"
        with open(signature_file, "wb") as sig_file:
            sig_file.write(binary_signature)
            logger("INFO", "cli:sign", f"Signature save on {self.owner}.sig")
        
        # Scans the public KeyboardInterruptardInterrupt
        pubkey = scan_public_key()

        # Create PEM data
        # Save PEM data to a file
        # with filename as owner's name
        pem = create_public_key_certificate(
            pubkey=pubkey,
            uncompressed=uncompreesed,
            owner=file_owner,
        )

        __pem_key_file__ = f"{args.file_owner}.pem"

        with open(file=__pem_key_file__, mode="w", encoding="utf-8") as pem_file:
            pem_file.write(pem)
            logger("INFO", "cli:sign", f"Public key certificate saved as '{__pem_key_file__}'")
            


class Verify:


    def verify(self):
        """
        onVerify is executed when `verify` command is called

        Args:
            :param parser
                the argument parser instance
        """ 
        verify_file(
            filename=args.verify_file,
            pubkey=args.pub_file,
            sigfile=args.sig_file,
        )

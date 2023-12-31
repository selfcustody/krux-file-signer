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
This python script is a tool to create air-gapped signatures of files using
a Krux device and convert hex publics exported from Krux to PEM public keys.
"""

####################
# Standart libraries
####################
import argparse

#################
# Local libraries
#################
from utils.constants import KSIGNER_VERSION, KSIGNER_CLI_DESCRIPTION
from cli.signer import Signer
from cli.verifyer import Verifyer

################
# Command parser
################
parser = argparse.ArgumentParser(
    prog="ksigner-cli", description=KSIGNER_CLI_DESCRIPTION
)

# Version
parser.add_argument(
    "-v", "--version", action="store_true", help="shows version", default=False
)

# Subparsers: sign and verify
subparsers = parser.add_subparsers(help="sub-command help", dest="command")

# Sign subparser commmand
signer = subparsers.add_parser("sign", help="sign a file")
signer.add_argument("-f", "--file", help="path to file to sign")
signer.add_argument(
    "-o",
    "--owner",
    help="the owner's name of public key certificate, i.e, the .pem file (default: 'pubkey')",
    default="pubkey",
)
signer.add_argument(
    "-u",
    "--uncompressed",
    action="store_true",
    help="flag to create a uncompreesed public key (default: False)",
)

# Verify subparsercommand
verifier = subparsers.add_parser("verify", help="verify signature")
verifier.add_argument("-f", "--file", help="path to file to verify")
verifier.add_argument("-s", "--sig-file", help="path to signature file")
verifier.add_argument("-p", "--pub-file", help="path to pubkey file")


if __name__ == "__main__":
    # parse arguments
    args = parser.parse_args()

    # on ksigner-cli --version
    if args.version:
        print(KSIGNER_VERSION)

    # on ksigner-cli --help
    elif args.command is None:
        parser.print_help()

    # on ksigner-cli sign --file <some file> [--owner <some owner>]
    elif args.command == "sign":
        signer = Signer(
            file=args.file, owner=args.owner, uncompressed=args.uncompressed
        )
        signer.sign()
        signer.make_pubkey_certificate()

    # on ksigner-cli verify \
    #                --file <some file> \
    #                --sig-file <some sig file> \
    #                --pub-file <some pub file>
    elif args.command == "verify":
        verifyer = Verifyer(
            file=args.file,
            pubkey=args.pub_file,
            signature=args.sig_file,
        )
        verifyer.build()
        result = verifyer.verify()
        print(result)

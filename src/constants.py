"""
constants.py

Some constants for the program 

For uncompressed and compressed string prependers,
see:

PUBKEY pre-String:
ASN.1 STRUCTURE FOR PUBKEY (uncompressed and compressed):
   30  <-- declares the start of an ASN.1 sequence
   56  <-- length of following sequence (dez 86)
   30  <-- length declaration is following
   10  <-- length of integer in bytes (dez 16)
   06  <-- declares the start of an "octet string"
   07  <-- length of integer in bytes (dez 7)
   2a 86 48 ce 3d 02 01 <-- Object Identifier: 1.2.840.10045.2.1
                            = ecPublicKey, ANSI X9.62 public key type
   06  <-- declares the start of an "octet string"
   05  <-- length of integer in bytes (dez 5)
   2b 81 04 00 0a <-- Object Identifier: 1.3.132.0.10
                      = secp256k1, SECG (Certicom) named eliptic curve
   03  <-- declares the start of an "octet string"
   42  <-- length of bit string to follow (66 bytes)
   00  <-- Start pubkey??

example for setup of 'pre' public key strings above:
   openssl ecparam -name secp256k1 -genkey -out ec-priv.pem
   openssl ec -in ec-priv.pem -pubout -out ec-pub.pem
   openssl ec -in ec-priv.pem -pubout -conv_form compressed -out ec-pub_c.pem
   cat ec-pub.pem
   cat ec-pub_c.pem
   echo "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEAd+5gxspjAfO7HA8qq0/    \
         7NbHrtTA3z9QNeI5TZ8v0l1pMJ1+mkg3d6zZVUXzMQZ/Y41iID+JAx/ \
         sQrY+wqVU/g==" | base64 -D - > ec-pub_uc.hex
   echo "MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgACAd+5gxspjAfO7HA8qq0/7Nb \
         HrtTA3z9QNeI5TZ8v0l0=" | base64 -D - > ec-pub_c.hex
   hexdump -C ec-pub_uc.hex
   hexdump -C ec-pub_c.hex

@see https://github.com/selfcustody/krux/blob/a63dc4ae917afc7ecd7773e6a4b13c23ea2da4d3/krux#L139
@see https://github.com/pebwindkraft/trx_cl_suite/blob/master/tcls_key2pem.sh#L134
"""

KSIGNER_VERSION = "0.0.1-alpha-0"
KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND = "3056301006072A8648CE3D020106052B8104000A034200"
KSIGNER_COMPRESSED_PUBKEY_PREPEND = "3036301006072A8648CE3D020106052B8104000A032200"
KSIGNER_CLI_DESCRIPTION = "".join(
    [
        "This python script is a tool to create air-gapped signatures of files using Krux. ",
        "The script can also convert hex publics exported from Krux to PEM public keys so ",
        "signatures can be verified using openssl.",
    ]
)

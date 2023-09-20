# Krux File Signer

Is a python script to help make airgapped signatures
and verification of signatures of any file with a 
supported device with krux firmware.

## Development

### Fetching the code

```bash
git clone https://github.com/selfcustody/krux-file-signer.git
```

### Install dev tools

The krux-file-signer code is a Python script
that should be installed with Poetry. To generate
a new `poetry.lock` file use: `poetry lock --no-update`.

With `pip`, you can do:

```bash
pip install poetry
poetry install
```

This will also install all development tools so that you can run pylint,
format code with black, and build an agnostic OS executable. 

### Format code

```bash
poetry run black ./src
```

### Lint code

```bash
poetry run pylint ./src
```

### Build executable

```bash
poetry run pyinstaller ./src/krux-file-signer.py
```

The generated executable will be placed on 
`dist/krux-file-signer/krux-file-signer`

### Commands

#### Help

Running `./dist/krux-file-signer/krux-file-signer --help` will show:

```bash
usage: krux_file_signer [-h] {sign,verify} ...

This python script is aimed to help and teach how Krux can be used to sign files and create PEM public keys so openssl can be used to verify

positional arguments:
  {sign,verify}  sub-command help
    sign         sign a file
    verify       verify signature

options:
  -h, --help     show this help message and exit
```

#### sign

Running `./dist/krux-file-signer/krux-file-signer sign --help`, will show:

```bash
usage: krux_file_signer sign [-h] [--file FILE_TO_SIGN]

options:
  -h, --help           show this help message and exit
  --file FILE_TO_SIGN  path to file to sign
```

#### verify

Running `/dist/krux-file-signer/krux-file-signer verify --help`, will show:

```bash
usage: krux_file_signer verify [-h] [--file VERIFY_FILE] [--sig-file SIG_FILE] [--pub-file PUB_FILE]

options:
  -h, --help           show this help message and exit
  --file VERIFY_FILE   path to file to verify
  --sig-file SIG_FILE  path to signature file
  --pub-file PUB_FILE  path to pubkey file
```
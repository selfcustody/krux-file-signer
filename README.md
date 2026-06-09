# Krux File Signer (aka __ksigner__)

Is a python script to help make airgapped signatures with Krux devices.
It also can verify the signatures.

## Development

### Fetching the code

```bash
git clone https://github.com/selfcustody/krux-file-signer.git
```

### Install dev tools

The `ksigner` code is a set of Python scripts whose dependencies are
managed with Poetry. To regenerate the `poetry.lock` file use: `poetry lock`.

With `pip`, you can do:

```bash
pip install poetry
poetry install
```

This will install all development tools so that you can run pylint and
format code with black.

### Format code

```bash
poetry run black ./src
```

### Lint code

```bash
poetry run pylint ./src
```

### Run

```bash
poetry run python src/ksigner.py --help
```

## Usage

### Commands

#### Help

Running `poetry run python src/ksigner.py --help` will show:

```bash
usage: ksigner [-h] [-v] [-V] [-n] [-g] {sign,verify} ...

This python script is a tool to create air-gapped signatures of files using
Krux. The script can also convert hex publics exported from Krux to PEM public
keys so signatures can be verified using openssl.

positional arguments:
  {sign,verify}     sub-command help
    sign            sign a file
    verify          verify signature

options:
  -h, --help        show this help message and exit
  -v, --version     shows version
  -V, --verbose     verbose output (default: False)
  -n, --normalize   normalizes the image of camera (default: False)
  -g, --gray-scale  apply gray-scale filter on camera's image (default: False)
```

#### sign

Running `poetry run python src/ksigner.py sign --help`, will show:

```bash
usage: ksigner sign [-h] -f FILE_TO_SIGN [-o FILE_OWNER] [-s SIG_FILE] [-u]

options:
  -h, --help            show this help message and exit
  -f FILE_TO_SIGN, --file FILE_TO_SIGN
                        path to file to sign
  -o FILE_OWNER, --owner FILE_OWNER
                        the owner's name of public key certificate, i.e, the
                        .pem file (default: 'pubkey')
  -s SIG_FILE, --sig-file SIG_FILE
                        path to save the signature file (default:
                        '<file_to_sign>.sig')
  -u, --uncompressed    flag to create a uncompreesed public key (default:
                        False)
```

#### verify

Running `poetry run python src/ksigner.py verify --help`, will show:

```bash
usage: ksigner verify [-h] -f VERIFY_FILE -s SIG_FILE -p PUB_FILE

options:
  -h, --help            show this help message and exit
  -f VERIFY_FILE, --file VERIFY_FILE
                        path to file to verify
  -s SIG_FILE, --sig-file SIG_FILE
                        path to signature file
  -p PUB_FILE, --pub-file PUB_FILE
                        path to pubkey file
```


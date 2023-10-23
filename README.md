# Krux File Signer (aka __ksigner__)

Is a python script to help make airgapped signatures with Krux devices.
It also can verify the signatures.

The project is divided in two _softwares_:

* `ksigner-cli`: is already able to sign and verify files.
* `ksigner-gui`: is under development with [`kivy` framework](https://kivy.org/) and shouldnt be used yet
 
## Development

### Fetching the code

```bash
git clone https://github.com/selfcustody/krux-file-signer.git
```

### Learn the flow of usage

This flow was made by [odudex](https://github.com/odudex) and is a helper
of usage and development.

<div>
  <image
    title="worflow"
    alt="Figure 1: Worflow of usage and development"
    src="assets/flow.jpg"
  >
  <p>Figure 1: Workflow of usage and development</p>
</div>

### Install dev tools

The `ksigner` suite is built as Python scripts with its dependencies
managed by [poetry](https://python-poetry.org/)


#### Install poetry and dependencies

Install [python-poetry](https://python-poetry.org/docs/)

*Linux*:

- pip: `pip install poetry`
- debian-like: `sudo apt-get -y install python3-poetry`
- archlinux-like: `sudo pacman -S python-poetry`
- fedora: `sudo dnf -y install poetry`

*MacOS* (TODO)
*Windows* (TODO)

##### Install pyzbar dependency

Before proceed you will need to install a dependency for pyzbar; in linux
it's `libzbar0` (see [this](https://stackoverflow.com/questions/63217735/import-pyzbar-pyzbar-unable-to-find-zbar-shared-library#63223900)):

*Linux*:

- debian-like: `sudo apt-get install -y libzbar0`
- archlinux-like: `sudo pacman -S zbar`
- fedora: `sudo dnf -y install zbar-libs`

*MacOS*

```bash
mkdir ~/lib
ln -s $(brew --prefix zbar)/lib/libzbar.dylib ~/lib/libzbar.dylib 
```

*Windows* (TODO)

#### Install poetry dependencies

This will also install all development tools so that you can run pylint,
format code with black, and build an agnostic OS executable. 

```bash
poetry install
```

#### Update lock file if already has one

Use this everytime you want to add a dependency.

```bash
poetry lock --no-update`
```

### Format code

```bash
poetry run black ./src
```

### Lint code

```bash
poetry run pylint ./src
```

### Developing executables

To run the suite as python scripts, you will need to use poetry correctly:

#### ksigner-cli

```bash
poetry run python src/ksigner-cli.py
```

#### ksigner-cli

```bash
poetry run python src/ksigner-gui.py
```

### Build executables

`ksigner` intends to be Operating System agnostic.
To achieve this goal, the project requires the correct use of pyinstaller:

#### `ksigner-cli` build

```bash
poetry run pyinstaller src/ksigner-cli.py
```

Will generate a executable placed on `dist/ksigner-cli/ksigner-cli`

#### `ksigner-gui` build

```bash
poetry run pyinstaller src/ksigner-gui.py
```

Will generate a executable placed on `dist/ksigner-gui/ksigner-gui`

## Usage

### `ksigner-cli`

Running `./dist/ksigner/ksigner --help` will show:

```bash
usage: ksigner-cli [-h] [-v] [-V] [-n] [-g] {sign,verify} ...

This python script is a tool to create air-gapped signatures of files using Krux. The script can also convert hex publics exported from Krux to PEM public keys so signatures can be verified using openssl.

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

Running `./dist/ksigner/ksigner sign --help`, will show:

```bash
usage: ksigner-cli sign [-h] [-f FILE_TO_SIGN] [-o FILE_OWNER] [-u]

options:
  -h, --help            show this help message and exit
  -f FILE_TO_SIGN, --file FILE_TO_SIGN
                        path to file to sign
  -o FILE_OWNER, --owner FILE_OWNER
                        the owner's name of public key certificate, i.e, the .pem file (default: 'pubkey')
  -u, --uncompressed    flag to create a uncompreesed public key (default: False)
```

#### verify

Running `/dist/krux-file-signer/krux-file-signer verify --help`, will show:

```bash
usage: ksigner-cli verify [-h] [-f VERIFY_FILE] [-s SIG_FILE] [-p PUB_FILE]

options:
  -h, --help            show this help message and exit
  -f VERIFY_FILE, --file VERIFY_FILE
                        path to file to verify
  -s SIG_FILE, --sig-file SIG_FILE
                        path to signature file
  -p PUB_FILE, --pub-file PUB_FILE
                        path to pubkey file

```

### `ksigner-gui`

*WARN*: this code is under development.

Its current status is shown in the animation below:

<div>
  <image
    title="ksigner-gui"
    alt="Figure 2: Current status of ksigner-gui"
    src="assets/ksigner-gui.gif"
  >
  <p>Figure 2: Current status of ksigner-gui</p>
</div>

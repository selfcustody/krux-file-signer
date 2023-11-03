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
kbuilder.py

Setup the PyInstaller module in a dynamic way
to proper configuration to build `src/ksigner-cli.py`
and `src/ksigner-gui.py` as standalone executables in 
`dist` folder
"""
import sys
from pathlib import Path
from platform import system
import PyInstaller.__main__

# Get root path of ksigners to properly setup
ROOT_PATH = Path(__file__).parent.parent.absolute()
pyname = f"ksigner-{sys.argv[1]}"
pyfile = f"{pyname}.py"
KFILE = str(ROOT_PATH / "src" / pyfile)

# build executable for following systems
if system() == "Linux":
    KNAME = f"{pyname}-linux"
elif system() == "Windows":
    KNAME = f"{pyname}-win.exe"
elif system() == "Darwin":
    KNAME = f"{pyname}-mac"
else:
    # pylint: disable=broad-exception-raised
    raise OSError(f"OS '{system()}' not implemented")

# Setup pyinstaller argumetns for cli executable
if sys.argv[1] == "cli":
    KBUILDER_ARGS = [KFILE, "--onefile", f"-n={KNAME}"]

# Setup pyinstaller argumetns for gui executable
elif sys.argv[1] == "gui":
    # We will need to add some datas from
    # kivy templates and ttf fonts
    # from local project, zbarcam and xcamera
    import os

    # pylint: disable=unused-import
    import kivy_garden.zbarcam

    # pylint: disable=unused-import
    import kivy_garden.xcamera

    ZBARCAM_PATH = os.path.dirname(sys.modules["kivy_garden.zbarcam"].__file__)
    XCAMERA_PATH = os.path.dirname(sys.modules["kivy_garden.xcamera"].__file__)

    KBUILDER_ARGS = [
        KFILE,
        "--add-data=src/ksigner.kv:.",
        "--add-data=src/terminus.ttf:.",
        f"--add-data={ZBARCAM_PATH}/*:kivy_garden/zbarcam",
        f"--add-data={XCAMERA_PATH}/*:kivy_garden/xcamera",
        f"--add-data={XCAMERA_PATH}/data/*.ttf:kivy_garden/xcamera/data",
        "--windowed",
        "--onefile",
        f"-n={KNAME}",
    ]

# Now build
PyInstaller.__main__.run(KBUILDER_ARGS)

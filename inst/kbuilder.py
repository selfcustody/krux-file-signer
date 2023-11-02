import sys
import PyInstaller.__main__
from pathlib import Path
from platform import system

ROOT_PATH = Path(__file__).parent.parent.absolute()
pyfile = "ksigner-%s.py" % sys.argv[1]
kfile = str(ROOT_PATH / "src" / pyfile)

if (system() == "Linux"):
    kname = "ksigner-%s-linux" % sys.argv[1]
if (system() == "Windows"):
    kname = "ksigner-%s-win.exe" % sys.argv[1]

if (sys.argv[1] == "cli"):
    KBUILDER_ARGS = [
        kfile,
        "--onefile",
        "-n=%s" % kname
    ]

elif (sys.argv[1] == "gui"):
    import os
    import kivy_garden.zbarcam
    import kivy_garden.xcamera
    
    ZBARCAM_PATH = os.path.dirname(sys.modules['kivy_garden.zbarcam'].__file__)
    XCAMERA_PATH = os.path.dirname(sys.modules['kivy_garden.xcamera'].__file__)
    
    KBUILDER_ARGS = [
        kfile,
        "--add-data=src/ksigner.kv:.",
        "--add-data=src/terminus.ttf:.",
        "--add-data=%s/*:kivy_garden/zbarcam" % ZBARCAM_PATH,
        "--add-data=%s/*:kivy_garden/xcamera" % XCAMERA_PATH,
        "--add-data=%s/data/*.ttf:kivy_garden/xcamera/data" % XCAMERA_PATH,
        "--windowed",
        "--onefile",
        "-n=%s" % kname
    ]

PyInstaller.__main__.run(KBUILDER_ARGS)


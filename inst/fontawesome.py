####################
# Standard libraries
####################
import sys
from pathlib import Path
from os import listdir
from os.path import isfile, join

#######################
# Thrid party libraries
#######################
import kivysome

URL = sys.argv[1]

ROOT_PATH = Path(__file__).parent.parent.absolute()
FONT_PATH = str(ROOT_PATH / "fonts")


print(f"Downloading {URL} -> {FONT_PATH}")
kivysome.enable(URL, group=kivysome.FontGroup.REGULAR, font_folder=FONT_PATH)

for f in listdir(FONT_PATH):
    __p__ = join(FONT_PATH, f)
    if isfile(__p__):
        print(f"Created {__p__}")

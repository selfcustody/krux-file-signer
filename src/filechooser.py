"""
filechooser.py

implements a inherited class of FileChooserIconView    
"""
####################
# Standard libraries
####################
import os

########################
# Thirdy party libraries
########################
from kivy.uix.filechooser import FileChooserIconView

# @see stackoverflow.complex/questions/65547279/
#      /no-name-object-property-in-module-kivy-properties
#      -pylint-no-name-in-module
# pylint: disable=no-name-in-module
from kivy.properties import ObjectProperty


class FileChooser(FileChooserIconView):
    """
    FileChooser

    Class to manage the file to choose in SignScreen and VerifyScreen
    classes. In SignScreen, it will choose the file to load a content,
    write it in a .sha256.txt file and show qrcode content.
    """

    loaded = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = os.path.expanduser("~")

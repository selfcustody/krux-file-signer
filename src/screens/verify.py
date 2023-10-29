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
verifyscreen.py

Implements an inherited kivy.uix.screenmanager.Screen
for verify signature options
"""
#######################
# Third party libraries
#######################
from kivy.uix.popup import Popup
# pylint: disable=no-name-in-module
from kivy.properties import StringProperty, ListProperty

#################
# Local libraries
#################
from screens.actioner import ActionerScreen
from screens.cacher import LoggedCache
from filechooser import LoadDialog

class VerifyScreen(ActionerScreen):
    """
    VerifyScreen

    Is a sub-widget, managed by KSignerApp@ScreenManager
    that executes signature verifications

    - [x] Load file
    - [x] Load signature
    - Load publickey
    - Verify signature
    """

    name = StringProperty("sign")
    """
    The screen's name 
    """

    popup_size_hint = ListProperty((0.9, 0.9))
    """
    Relative size of file popup
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_file_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_file_popup.dismiss,
            on_submit=self.on_submit_file_to_be_verified,
         )
        self._load_file_popup = Popup(
            title="Load a file to be verified",
            content=self._load_file_dialog,
            size_hint=self.popup_size_hint
        )
    
    def on_press_load_file(self):
        """
        Change background color of :data:`verify_screen_load_file_button` widget
        """
        self._on_press(id="verify_screen_load_file_button")

    def on_release_load_file(self):
        """
        Change background of :data:`verifu_screen_load_file_button` widget
        and open popup to choose file
        """
        self._on_release(id="verify_screen_load_file_button")
        self.info("opening <Popup>")
        self._load_file_popup.open()

    def on_submit_file_to_be_verified(self, *args):
        """
        Cache file name to be verified
        """        
        # cache file input
        LoggedCache.append("ksigner", "file_input", args[1][0])

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._load_file_popup.dismiss()

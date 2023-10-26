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
signscreen.py

An inherited implementations of kivy.uix.screenmanager Screen    
"""
#####################
# Thirparty libraries
#####################
from kivy.uix.popup import Popup

# pylint: disable=no-name-in-module
from kivy.properties import StringProperty, ListProperty
from kivy.logger import LOG_LEVELS

#################
# Local libraries
#################
from screens.actioner import ActionerScreen
from cli.signer import Signer
from filechooser import LoadDialog


class SignScreen(ActionerScreen):
    """
    SignScreen

    Class to manage the creation of signatures. It has 4 buttons:

    - Load File & export hash QRCode: `show_load` method;
    - Import & save signature: `TODO`;
    - Import & save publickey: `TODO`;
    - Back: `__on_release__` method
    """

    file_input = StringProperty("")
    """
    The input file to be hashed
    """

    file_content = StringProperty("")
    """
    The content of file input to be hashed
    """

    file_hash = StringProperty("")
    """
    The hash of file input
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
        self._content = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._popup.dismiss,
            on_submit=self.on_submit_file,
        )
        self._popup = Popup(
            title="Load a file",
            content=self._content,
            size_hint=self.popup_size_hint
        )

        
    def on_press_sign_screen_load_file_and_export_hash_qrcode(self):
        """
        Change background color of
        :data:`sign_screen_load_file_and_export_hash_qrcode` widget
        """
        self._on_press(id="sign_screen_load_file_and_export_hash_qrcode")
        
    def on_release_sign_screen_load_file_and_export_hash_qrcode(self):
        """
        Change background of 
        :data:`sign_screen_load_file_and_export_hash_qrcode` widget
        and open popup to choose file
        """
        self._on_release(id="sign_screen_load_file_and_export_hash_qrcode")
        self.info("opening <Popup>")
        self._popup.open()

    def on_press_sign_screen_import_and_save_signature(self):
        """
        Change background of 
        :data:`sign_screen_import_and_save_signature` widget
        """
        self._on_press(id="sign_screen_import_and_save_signature")

    def on_release_sign_screen_import_and_save_signature(self):
        """
        Change background of 
        :data:`sign_screen_import_and_save_signature` widget
        and redirects to :data:`scan-import-save-signature`
        screen
        """
        self._on_release(id="sign_screen_import_and_save_signature")
        self._set_transition(direction="right")
        self._set_current(screen="scan-import-save-signature")

    def on_press_sign_screen_import_and_save_public_key(self):
        """
        Change background of 
        :data:`sign_screen_import_and_save_public_key` widget
         """
        self._on_press(id="sign_screen_import_and_save_public_key")

    def on_release_sign_screen_import_and_save_public_key(self):
        """
        Change background of 
        :data:`sign_screen_import_and_save_public_key` widget
        and redirects to :data:`scan-import-save-public-key`
        screen
        """
        self._on_release(id="sign_screen_import_and_save_public_key")
        self._set_transition(direction="right")
        self._set_current(screen="scan-import-save-public-key")

    def on_press_back_main(self):
        """
        Change background of 
        :data:`sign_screen_back` widget
        """
        self._on_press(id="sign_screen_back")

    def on_release_back_main(self):
        """
        Change background of 
        :data:`sign_screen_back` widget
        on_release_back_main
        """
        self._on_release(id="sign_screen_back")
        self._set_transition(direction="left")
        self._set_current(screen="main")

    def on_submit_file(self, *args):
        """
        Call :class:`Signer` to open, read and hash
        (sha256sum) a given file and redirect to QRCodeScreen
        """
        # cache file input
        self.file_input = args[1][0]
        msg = "<Popup> loading %s" % self.file_input
        self.info(msg)

        # Use cli.signer module
        # to implement signature on GUI
        if (self.loglevel == LOG_LEVELS["debug"]):
            loglevel = "debug"
        elif (self.loglevel == LOG_LEVELS["warning"]):
            loglevel = "warning"
        elif (self.loglevel == LOG_LEVELS["error"]):
            loglevel = "error"
        else:
            loglevel = "info"
            
        signer = Signer(
            file=self.file_input,
            owner=self.file_input,
            uncompressed=False,
            loglevel=loglevel,
        )

        # Saves the hash in a .sha256sum file
        self.file_hash = signer.hash_file()
        signer.save_hash_file(self.file_hash)

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._popup.dismiss()

        # Cache qrcode data
        msg = "Caching filename and hash to <QRCodeScreen>"
        self.info(msg)
        qrcodescreen = self.manager.get_screen("qrcode")
        qrcodescreen.text = f"[b]{self.file_input}[/b]\n\n[b]{self.file_hash}[/b]"
        qrcodescreen.code = self.file_hash

        # Change the screen
        self._set_screen(name="qrcode", direction="left")

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

#################
# Local libraries
#################
from screens.actioner import ActionerScreen
from screens.cacher import LoggedCache
from cli.signer import Signer
from filechooser import LoadDialog


# pylint: disable=too-many-ancestors
class SignScreen(ActionerScreen):
    """
    SignScreen

    Class to manage the creation of signatures. It has 4 buttons:

    - Load File & export hash QRCode: `show_load` method;
    - Import & save signature: `TODO`;
    - Import & save publickey: `TODO`;
    - Back: `__on_release__` method
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
            title="Load a file", content=self._content, size_hint=self.popup_size_hint
        )

    def on_press_export_sha256_message(self):
        """
        Change background color of :data:`export_sha256_message` widget
        """
        self._on_press(id="export_sha256_message")

    def on_release_export_sha256_message(self):
        """
        Change background of :data:`export_sha256_message` widget
        and open popup to choose file
        """
        self._on_release(id="export_sha256_message")
        self.info("opening <Popup>")
        self._popup.open()

    def on_press_import_signature_message(self):
        """
        Change background of :data:`import_signature_message` widget
        """
        self._on_press(id="import_signature_message")

    def on_release_import_signature_message(self):
        """
        Change background of :data:`import_signature_message` widget
        and redirects to :data:`import_signature_message` screen
        """
        self._on_release(id="import_signature_message")
        self._set_screen(name="import-signature", direction="right")

    def on_press_import_publickey_message(self):
        """
        Change background of
        :data:`import_publickey_message` widget
        """
        self._on_press(id="import_publickey_message")

    def on_release_import_publickey_message(self):
        """
        Change background of :data:`import_publickey_message` widget
        and redirects to :data:`import-public-key` screen
        """
        self._on_release(id="import_publickey_message")
        self._set_screen(name="import-public-key", direction="right")

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
        self._set_screen(name="main", direction="right")

    def on_submit_file(self, *args):
        """
        Call :class:`Signer` to open, read and hash
        (sha256sum) a given file and redirect to QRCodeScreen
        """
        # cache file input
        LoggedCache.append("ksigner", "file_input", args[1][0])
        LoggedCache.append("ksigner", "owner", args[1][0])
        file_input = LoggedCache.get("ksigner", "file_input")
        owner = LoggedCache.get("ksigner", "owner")

        msg = f"<Popup> loading {file_input}"
        self.info(msg)

        signer = Signer(
            file=file_input,
            owner=owner,
            uncompressed=False,
        )

        # Cache the hash in a .sha256sum file
        _hash = signer.hash_file()
        LoggedCache.append("ksigner", "hash", _hash)

        # Cache the hashed file
        hash_file = f"{file_input}.sha256sum.txt"
        LoggedCache.append("ksigner", "hash_file", hash_file)
        signer.save_hash_file(hash_file)

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._popup.dismiss()

        # Change the screen
        self._set_screen(name="export-sha256", direction="left")

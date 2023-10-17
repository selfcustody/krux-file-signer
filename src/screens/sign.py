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
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

# pylint: disable=no-name-in-module
from kivy.properties import StringProperty

#################
# Local libraries
#################
from utils.log import logger
from utils.hash import open_and_hash_file
from filechooser import LoadDialog


class SignScreen(Screen):
    """
    SignScreen

    Class to manage the creation of signatures. It has 4 buttons:

    - Load File & export hash QRCode: `show_load` method;
    - Import & save signature: `TODO`;
    - Import & save publickey: `TODO`;
    - Back: `__on_release__` method
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._content = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._popup.dismiss,
            on_submit=self.on_submit_file,
        )
        self._popup = Popup(
            title="Load a file", content=self._content, size_hint=(0.9, 0.9)
        )
        self.file_input = StringProperty("")
        self.file_content = StringProperty("")
        self.file_hash = StringProperty("")

    def on_press_sign_screen_load_file_and_export_hash_qrcode(self):
        """
        on_press_sign_screen_load_file_and_export_hash_qrcode

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        logger(
            "DEBUG",
            "SignScreen: <Button::sign_screen_load_file_and_export_hash_qrcode> clicked",
        )
        self.ids.sign_screen_load_file_and_export_hash_qrcode.background_color = (
            0.5,
            0.5,
            0.5,
            0.5,
        )

    def on_release_sign_screen_load_file_and_export_hash_qrcode(self):
        """
        on_release_sign_screen_load_file_and_export_hash_qrcode

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - open the FileChooser popup
        """
        logger(
            "DEBUG",
            "SignScreen: <Button::sign_screen_load_file_and_export_hash_qrcode> released",
        )
        self.ids.sign_screen_load_file_and_export_hash_qrcode.background_color = (
            0,
            0,
            0,
            0,
        )

        logger("DEBUG", "SignScreen: <Popup> opening")
        self._popup.open()

    def on_press_sign_screen_import_and_save_signature(self):
        """
        on_press_import_and_save_signature

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        logger(
            "DEBUG",
            "SignScreen: <Button::sign_screen_import_and_save_signature> pressed",
        )
        self.ids.sign_screen_import_and_save_signature.background_color = (
            0.5,
            0.5,
            0.5,
            0.5,
        )

    def on_release_sign_screen_import_and_save_signature(self):
        """
        on_release_sign_screen_import_and_save_signature

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'pressed'
        - go to ScanScreen
        """
        logger(
            "DEBUG",
            "SignScreen: <Button::sign_screen_import_and_save_signature> released",
        )
        self.ids.sign_screen_load_file_and_export_hash_qrcode.background_color = (
            0,
            0,
            0,
            0,
        )
        self
        self.manager.transition.direction = "right"
        self.manager.current = "scan-import-save-signature"

    def on_press_sign_screen_import_and_save_public_key(self):
        """
        on_press_import_and_save_public_key

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        logger(
            "DEBUG",
            "SignScreen: <Button::sign_screen_import_and_save_public_key> pressed",
        )
        self.ids.sign_screen_import_and_save_public_key.background_color = (
            0.5,
            0.5,
            0.5,
            0.5,
        )

    def on_release_sign_screen_import_and_save_public_key(self):
        """
        on_release_sign_screen_import_and_save_public_key

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'pressed'
        - go to ScanScreen
        """
        logger(
            "DEBUG",
            "SignScreen: <Button::sign_screen_import_and_save_public_key> released",
        )
        self.ids.sign_screen_import_and_save_public_key.background_color = (
            0,
            0,
            0,
            0,
        )
        self
        self.manager.transition.direction = "right"
        self.manager.current = "scan-import-save-signature"

    def on_press_back_main(self):
        """
        on_press_back_main

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        logger("DEBUG", "SignScreen: <Button::back> pressed")
        self.ids.sign_screen_back.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_back_main(self):
        """
        on_release_back_main

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        - go back to MainScreen
        """
        logger("DEBUG", "SignScreen: <Button::back> released")
        self.ids.sign_screen_back.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def on_submit_file(self, *args):
        """
        on_submit_file

        Call `open_and_hash_file` to open, read and hash (sha256sum)
        a given file and redirect to QRCodeScreen
        """
        self.file_input = args[1][0]
        logger("DEBUG", f"SignScreen: <Popup> loading {self.file_input}")

        self.file_hash = open_and_hash_file(path=self.file_input, verbose=True)

        logger("DEBUG", "SignScreen: <Popup> closed")
        self._popup.dismiss()

        logger("DEBUG", "SignScreen: Caching filename and hash to <QRCodeScreen>")
        qrcodescreen = self.manager.get_screen("qrcode")
        qrcodescreen.text = f"[b]{self.file_input}[/b]\n\n[b]{self.file_hash}[/b]"
        qrcodescreen.code = self.file_hash

        logger("DEBUG", "SignScreen: Redirecting to <QRCodeScreen>")
        self.manager.transition.direction = "left"
        self.manager.current = "qrcode"

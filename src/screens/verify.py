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
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# pylint: disable=no-name-in-module
from kivy.properties import StringProperty, ListProperty

#################
# Local libraries
#################
from cli.verifyer import Verifyer
from screens.actioner import ActionerScreen
from screens.cacher import LoggedCache
from filechooser import LoadDialog


# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
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

    file_to_be_verified_message_text = StringProperty("Load file to be verified")
    """
    File to be verified message text
    """

    file_signature_to_verify_message_text = StringProperty("Load Signature")
    """
    Signature file message text
    """

    file_pubkey_to_verify_message_text = StringProperty("Load Public Key")
    """
    Public key file message text
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # File to be verified LoadDialog and Popup
        self._load_file_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_file_popup.dismiss,
            on_submit=self.on_submit_file_to_be_verified,
        )
        self._load_file_popup = Popup(
            title="Load a file to be verified",
            content=self._load_file_dialog,
            size_hint=self.popup_size_hint,
        )

        # Signature's file to be verified LoadDialog and Popup
        self._load_signature_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_signature_popup.dismiss,
            on_submit=self.on_submit_signature,
        )
        self._load_signature_popup = Popup(
            title="Load the signature's file to be verified",
            content=self._load_signature_dialog,
            size_hint=self.popup_size_hint,
        )

        # Public key certificate's file to be verified LoadDialog and Popup
        self._load_pubkey_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_pubkey_popup.dismiss,
            on_submit=self.on_submit_pubkey,
        )
        self._load_pubkey_popup = Popup(
            title="Load the public-key certificate's file to be verified",
            content=self._load_pubkey_dialog,
            size_hint=self.popup_size_hint,
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

        if args[1][0] is not None:
            _icon = self._build_check_icon(color="00ff00", font_name="fa-regular-6.4.2")
            self.file_to_be_verified_message_text = " ".join(
                [_icon, self.file_to_be_verified_message_text]
            )

            self.debug(f"new button text '{self.file_to_be_verified_message_text}'")

    def on_press_load_signature(self):
        """
        Change background color of :data:`verify_screen_load_signature` widget
        """
        self._on_press(id="verify_screen_load_signature")

    def on_release_load_signature(self):
        """
        Change background of :data:`verify_screen_load_signature` widget
        and open popup to choose file
        """
        self._on_release(id="verify_screen_load_signature")
        self.info("opening <Popup>")
        self._load_signature_popup.open()

    def on_submit_signature(self, *args):
        """
        Cache signature's file be verified
        """
        # cache file input
        LoggedCache.append("ksigner", "signature", args[1][0])

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._load_signature_popup.dismiss()

        if not args[1][0].endswith(".sig"):
            message = "\n".join([
                f"'{args[1][0]}' do not have a valid extension.",
                "Valid files ends with '.sig'"
            ])
            self._make_alert(title="Invalid file", message=message)
            self.file_signature_to_verify_message_text = "Load Signature"

        elif args[1][0] is not None:
            _icon = self._build_check_icon(color="00ff00", font_name="fa-regular-6.4.2")
            self.file_signature_to_verify_message_text = " ".join(
                [_icon, self.file_signature_to_verify_message_text]
            )

            self.debug(
                f"new button text '{self.file_signature_to_verify_message_text}'"
            )

    def on_press_load_pubkey(self):
        """
        Change background color of :data:`verify_screen_load_pubkey` widget
        """
        self._on_press(id="verify_screen_load_pubkey")

    def on_release_load_pubkey(self):
        """
        Change background of :data:`verify_screen_load_pubkey` widget
        and open popup to choose file
        """
        self._on_release(id="verify_screen_load_pubkey")
        self.info("opening <Popup>")
        self._load_pubkey_popup.open()

    def on_submit_pubkey(self, *args):
        """
        Cache public key certificate's file be verified
        """
        # cache file input
        LoggedCache.append("ksigner", "pubkey", args[1][0])

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._load_pubkey_popup.dismiss()

        if not args[1][0].endswith(".pem"):
            message = "\n".join([
                f"'{args[1][0]}' do not have a valid extension.",
                "Valid files ends with '.pem'"
            ])
            self._make_alert(title="Invalid file", message=message)
            self.file_pubkey_to_verify_message_text = "Load Public Key"
            
        elif args[1][0] is not None:
            _icon = self._build_check_icon(color="00ff00", font_name="fa-regular-6.4.2")
            self.file_pubkey_to_verify_message_text = " ".join(
                [_icon, self.file_pubkey_to_verify_message_text]
            )

            self.debug(f"new button text '{self.file_pubkey_to_verify_message_text}'")

    def on_press_verify(self):
        """
        Change background color of :data:`verify_screen_verification` widget
        """
        self._on_press(id="verify_screen_verification")

    def on_release_verify(self):
        """
        Change background of :data:`verify_screen_verification` widget
        and open popup to choose file
        """
        self._on_release(id="verify_screen_verification")

        # Get caches
        file = LoggedCache.get("ksigner", "file_input")
        sig = LoggedCache.get("ksigner", "signature")
        pub = LoggedCache.get("ksigner", "pubkey")

        # Verify
        self.debug("Building verification")
        verifyer = Verifyer(file=file, signature=sig, pubkey=pub)

        command = verifyer.make_openssl_command()
        result = verifyer.verify(command)
        msg = f"verification result: {result}"
        self.info(msg)

        # Verification popup
        self.debug("Creating <BoxLayout> for <Popup>")
        _verification_box_popup = BoxLayout(orientation="vertical")

        # show an alert
        text = "\n".join(("" f"[b]{self._chunk_str(command, 88)}[/b]", "", result))
        self._make_alert(title="Verification result", message=text, markup=True)        


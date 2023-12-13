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
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

# pylint: disable=no-name-in-module
from kivy.properties import StringProperty, ListProperty

#################
# Local libraries
#################
from cli.verifyer import Verifyer
from screens.actioner import ActionerScreen
from screens.cacher import LoggedCache
from utils.filechooser import LoadDialog


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

    popup_size_hint = ListProperty((0.9, 0.9))
    """
    Relative size of file popup
    """

    verify_screen_load_file_text = StringProperty(
        "Drop a file or click to load one to be verified"
    )

    verify_screen_load_signature_text = StringProperty(
        "Drop a file or click to load a signature"
    )

    verify_screen_load_pubkey_text = StringProperty(
        "Drop a file or click to load the public key"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_public_key_popup = None
        self._load_public_key_dialog = None
        self._set_load_screen_dialog()
        self._set_load_file_popup()
        self._set_load_signature_dialog()
        self._set_load_signature_popup()
        self._set_load_signature_dialog()
        self._set_load_signature_popup()

        # pylint: disable=unused-argument
        def _on_drop_file(window, filename, x_pos, y_pos, *args):
            """
            Callback for when user drag a file to window in a specifig button
            """
            vs_file = self.ids["verify_screen_load_file"]
            vs_sig = self.ids["verify_screen_load_signature"]
            vs_pub = self.ids["verify_screen_load_pubkey"]

            _filename = filename.decode("utf-8")

            # pylint: disable=chained-comparison
            if y_pos > 0 and y_pos < vs_file.height:
                # log some data
                self.debug(
                    " ".join(
                        [
                            f"{_filename} dropped on",
                            "'verify_screen_load_file' at position",
                            f"({x_pos}, {y_pos})",
                        ]
                    )
                )
                self._on_submit_file_to_be_verified(filename=_filename)

            # pylint: disable=chained-comparison
            if y_pos > vs_file.height and y_pos < (vs_file.height + vs_sig.height):
                self.debug(
                    " ".join(
                        [
                            f"{_filename} dropped on",
                            "'verify_screen_load_signature' at position",
                            f"({x_pos}, {y_pos})",
                        ]
                    )
                )
                self._on_submit_signature(filename=_filename)

            # pylint: disable=chained-comparison
            if y_pos > (vs_file.height + vs_sig.height) and y_pos < (
                vs_file.height + vs_sig.height + vs_pub.height
            ):
                self.debug(
                    " ".join(
                        [
                            f"{_filename} dropped on ",
                            "'verify_screen_load_pubkey' at position",
                            f"({x_pos}, {y_pos})",
                        ]
                    )
                )
                self._on_submit_public_key(filename=_filename)

        Window.bind(on_drop_file=_on_drop_file)

    def _set_load_screen_dialog(self):
        # File to be verified LoadDialog and Popup
        self._load_file_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_file_popup.dismiss,
            on_submit=self.on_submit_file_to_be_verified,
        )

    def _set_load_file_popup(self):
        self._load_file_popup = Popup(
            title="Load a file to be verified",
            content=self._load_file_dialog,
            size_hint=self.popup_size_hint,
        )

    def _set_load_signature_dialog(self):
        # Signature's file to be verified LoadDialog and Popup
        self._load_signature_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_signature_popup.dismiss,
            on_submit=self.on_submit_signature,
        )

    def _set_load_signature_popup(self):
        self._load_signature_popup = Popup(
            title="Load the signature's file to be verified",
            content=self._load_signature_dialog,
            size_hint=self.popup_size_hint,
        )

    def _set_load_public_key_dialog(self):
        # Public key certificate's file to be verified LoadDialog and Popup
        self._load_public_key_dialog = LoadDialog(
            load=LoadDialog.load,
            cancel=lambda: self._load_public_key_popup.dismiss,
            on_submit=self.on_submit_public_key,
        )

    def _set_load_public_key_popup(self):
        self._load_public_key_popup = Popup(
            title="Load the public-key certificate's file to be verified",
            content=self._load_public_key_dialog,
            size_hint=self.popup_size_hint,
        )

    def _add_icon(self, **kwargs):
        """
        Add a check icon to button that load file to be verified
        """
        _id = kwargs.get("id")
        text = kwargs.get("text")
        _icon = self._build_check_icon(color="00ff00", font_name="fa-regular-6.4.2")
        textid = f"{_id}_text"
        setattr(self, textid, f"{_icon} {text}")
        self.debug(f"new button text '{getattr(self, textid)}'")

    def _on_submit_file_to_be_verified(self, **kwargs):
        """
        Cache filename to be verified and changes icon
        """
        filename = kwargs.get("filename")
        LoggedCache.append("ksigner", "file_input", filename)

        # Change icon
        self._add_icon(id="verify_screen_load_file", text="File to be verified loaded")

    def _on_submit_signature(self, **kwargs):
        """
        Check if its is a valid signature file,
        cache signature's file to be verified
        """
        # cache file input
        filename = kwargs.get("filename")

        if not filename.endswith(".sig"):
            message = "\n".join(
                [
                    f"'{filename}' do not have a valid extension.",
                    "Valid files ends with '.sig'",
                ]
            )
            self._make_alert(title="Invalid file", message=message)
            self.file_signature_to_verify_message_text = "Load Signature"

        else:
            LoggedCache.append("ksigner", "signature", filename)
            self._add_icon(
                id="verify_screen_load_signature", text="Signature file loaded"
            )

    def _on_submit_public_key(self, **kwargs):
        """
        Check if its is a valid public key file,
        cache public key's file to be verified
        """
        # cache file input
        filename = kwargs.get("filename")

        if not filename.endswith(".pem"):
            message = "\n".join(
                [
                    f"'{filename}' do not have a valid extension.",
                    "Valid files ends with '.pem'",
                ]
            )
            self._make_alert(title="Invalid file", message=message)
            self.file_signature_to_verify_message_text = "Load Signature"

        else:
            LoggedCache.append("ksigner", "pubkey", filename)
            self._add_icon(
                id="verify_screen_load_pubkey",
                text="Public key certificate file loaded",
            )

    def _on_verify(self, **kwargs):
        file = kwargs.get("file")
        sig = kwargs.get("signature")
        pub = kwargs.get("pubkey")

        # Verify
        self.debug("Building verification")
        verifyer = Verifyer(file=file, signature=sig, pubkey=pub)

        result = verifyer.verify()
        msg = f"verification result: {result}"
        self.info(msg)

        # Verification popup
        self.debug("Creating <BoxLayout> for <Popup>")
        _verification_box_popup = BoxLayout(orientation="vertical")

        # show an alert
        self._make_alert(title="Verification result", message=result, markup=True)

    def on_press_load_file(self):
        """
        Change background color of :data:`verify_screen_load_file_button` widget
        """
        self._on_press(id="verify_screen_load_file")

    def on_release_load_file(self):
        """
        Change background of :data:`verifu_screen_load_file_button` widget
        and open popup to choose file
        """
        self._on_release(id="verify_screen_load_file")
        self.info("opening <Popup>")
        self._load_file_popup.open()

    def on_submit_file_to_be_verified(self, *args):
        """
        Cache filename to be verified, changes icon
        and close a popup
        """
        self._on_submit_file_to_be_verified(filename=args[1][0])

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._load_file_popup.dismiss()

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
        Check if its is a valid signature file,
        cache signature's file to be verified
        and close a popup
        """
        self._on_submit_signature(filename=args[1][0])

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._load_signature_popup.dismiss()

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
        self._load_public_key_popup.open()

    def on_submit_public_key(self, *args):
        """
        Check if its is a valid public key file,
        cache public key's file to be verified
        and close a popup
        """
        self._on_submit_signature(filename=args[1][0])

        # Close the popup
        msg = "Closing <Popup>"
        self.info(msg)
        self._load_public_key_popup.dismiss()

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

        print(file)
        msg = []
        if file is None:
            msg.append("File to be verified cannot be 'None'")

        if sig is None:
            msg.append("Signature file cannot be 'None'")

        if pub is None:
            msg.append("Public key certificate cannot be 'None'")

        if len(msg) > 0:
            self._make_alert(
                title="Verification cannot be done", message="\n\n".join(msg)
            )
        else:
            self._on_verify(file=file, signature=sig, pubkey=pub)

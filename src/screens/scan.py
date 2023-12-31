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
scan.py

Implements an inherited kivy.uix.screenmanager.Screen
for scan QRCodes
"""
import sys
import os

################
# Kivy libraries
################
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy_garden.zbarcam import ZBarCam

#################
# Local libraries
#################
from screens.actioner import ActionerScreen
from screens.cacher import LoggedCache
from cli.signer import Signer


# pylint: disable=too-many-ancestors
class ScanScreen(ActionerScreen):
    """
    Class to implement a scanner widget
    """

    zbar_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.5})
    """
    :data:`label_pos_hint` is a 
    :class:`~kivy.properties.ObjectProperty`,
    to set the default position on Screen
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Widgets
        self._box_layout = None
        self._zbarcam = None

    def on_pre_enter(self, *args):
        """
        Event fired when the screen is about to be used: the entering animation is started.
        """
        self._zbarcam = ZBarCam()
        self.add_widget(self._zbarcam)
        self.info("<ZBarCam> added")
        Clock.schedule_interval(self._decode_qrcode, 1)

    def _alert(self, **kwargs):
        title = kwargs.get("title")
        message = kwargs.get("message")

        # Verification popup
        self.debug("Creating <Popup::BoxLayout>")
        _box_popup = BoxLayout(orientation="vertical")

        _label_popup = Label(text=message, markup=True)
        msg = f"Creating <Popup::Label> text='{message}'"
        self.debug(msg)

        self.debug("Adding <Popup::BoxLayout>")
        _box_popup.add_widget(_label_popup)

        self.debug("Creating <Popup>")
        _popup = Popup(
            title=title,
            title_align="center",
            content=_box_popup,
            size_hint=(0.9, 0.9),
            auto_dismiss=True,
        )

        _button = Button(text="Back", on_press=lambda *args: _popup.dismiss())

        self.debug("Adding <Popup::Button>")
        _box_popup.add_widget(_button)

        self.info("opening <Popup>")
        _popup.open()

    # pylint: disable=unused-argument
    def _decode_qrcode(self, *args):
        """
        When camera capture the QRCode, :data:`zbarcam.symbols`
        will be feeded to :class:`Signer` and saved as `.sig`
        or `.pem` files. When it occurs, stop scanning
        """
        self.debug("Waiting for qrcode")
        if len(self._zbarcam.symbols) > 0:
            scanned_data = self._zbarcam.symbols[0].data.decode("UTF-8")
            msg = f"captured '{scanned_data}'"
            self.info(msg)

            # Get cached data
            file_input = LoggedCache.get("ksigner", "file_input")
            owner = LoggedCache.get("ksigner", "owner")

            if self.manager.current == "import-signature":
                self.debug("Saving signature")
                signer = Signer(file=file_input, owner=owner, uncompressed=False)

                signer.save_signature(scanned_data)
                title = "Signature saved"
                self._alert(title=title, message=f"{file_input}.sig")

            elif self.manager.current == "import-public-key":
                self.debug("Saving publickey certificate")
                signer = Signer(file=file_input, owner=owner, uncompressed=False)
                signer.save_pubkey_certificate(scanned_data)
                title = "Public key saved"
                self._alert(title=title, message=f"{file_input}.pem")

            else:
                msg = f"Invalid screen '{self.manager.screen}'"
                self.debug(msg)

            self.debug("Unscheduling QRCode decodification")
            Clock.unschedule(self._decode_qrcode, 1)

            self.debug("Releasing device")
            # pylint: disable=protected-access
            self._zbarcam.ids.xcamera._camera._device.release()

            self.debug("Stopping <ZBarCam>")
            self._zbarcam.stop()  # stop zbarcam

            # unload zbarcam.kv file
            mod_path = os.path.dirname(sys.modules["kivy_garden.zbarcam"].__file__)
            zbar_kv_path = os.path.join(mod_path, "zbarcam.kv")
            msg = f"Unloading '{zbar_kv_path}'"
            self.debug(msg)
            Builder.unload_file(zbar_kv_path)

            # unload xcamera.kv file
            mod_path = os.path.dirname(sys.modules["kivy_garden.xcamera"].__file__)
            xcam_kv_path = os.path.join(mod_path, "xcamera.kv")
            msg = f"Unloading '{xcam_kv_path}'"
            self.debug(msg)
            Builder.unload_file(xcam_kv_path)

            # Now create some glyph icon to button
            _icon = self._build_check_icon(color="00ff00", font_name="fa-regular-6.4.2")

            # add the glyph icon to button text
            sign_screen = self.manager.get_screen("sign")

            if self.manager.current == "import-signature":
                _text = f"{_icon} {sign_screen.import_signature_message_text}"
                setattr(sign_screen, "import_signature_message_text", _text)
            if self.manager.current == "import-public-key":
                _text = f"{_icon} {sign_screen.import_publickey_message_text}"
                setattr(sign_screen, "import_publickey_message_text", _text)

            self._set_screen(name="sign", direction="right")

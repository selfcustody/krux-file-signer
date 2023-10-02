"""
signscreen.py

An inherited implementations of kivy.uix.screenmanager Screen    
"""
import os
import tempfile

#####################
# Thirparty libraries
#####################
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

# @see stackoverflow.complex/questions/65547279/
#      /no-name-object-property-in-module-kivy-properties
#      -pylint-no-name-in-module
# pylint: disable=no-name-in-module
from kivy.properties import StringProperty
from kivy.uix.image import Image
import qrcode

#################
# Local libraries
#################
from logutils import verbose_log
from hashutils import open_and_hash_file
from qrutils import encode_to_string
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
            title="Load a file",
            content=self._content,
            size_hint=(0.9, 0.9)
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
        verbose_log(
            "INFO",
            "<SignScreen@Button::sign_screen_load_file_and_export_hash_qrcode> clicked",
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
        verbose_log(
            "INFO",
            "<SignScreen@Button::sign_screen_load_file_and_export_hash_qrcode> released",
        )
        self.ids.sign_screen_load_file_and_export_hash_qrcode.background_color = (
            0,
            0,
            0,
            0,
        )

        verbose_log("INFO", "<SignScreen@Popup> opening")
        self._popup.open()

    def on_press_back_main(self):
        """
        on_press_back_main

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        verbose_log("INFO", "Clicking <SignScreen@Button::Back>")
        self.ids.sign_screen_back.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_back_main(self):
        """
        on_release_back_main

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        - go back to MainScreen
        """
        verbose_log("INFO", "Clicking <SignScreen@Button::Back>")
        self.ids.sign_screen_back.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def on_submit_file(self, *args):
        """
        on_submit_file

        Call `open_and_hash_file` to open, read and hash (sha256sum)
        a given file   
        """
        self.file_input = args[1][0]
        
        verbose_log("INFO", f"<SignScreen@Popup> loading {self.file_input}")
        self.file_hash = open_and_hash_file(path=self.file_input, verbose=True)
        
        verbose_log("INFO", f"<SignScreen@Popup> hash: {self.file_hash}")
        self._popup.dismiss()

        verbose_log("INFO", "<SignScreen> converting to QRCode")
        qr_binary_data = encode_to_string(self.file_hash)
        verbose_log("INFO", "<SignScreen> Raw data: "+ "".join(qr_binary_data))
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(qr_binary_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_path = os.path.join(tempfile.gettempdir(), f"{self.file_input}.png")
        verbose_log("INFO", f"<SignScreen> Saving on: {img_path}")
        img.save(img_path)
        
        self._popup = Popup(
            title=self.file_input,
            content=Image(source=img_path),
            size_hint=(None, None),
            size=(400, 400)
        )

        self._popup.open()
        
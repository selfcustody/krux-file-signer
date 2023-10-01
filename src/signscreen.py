"""
signscreen.py

An inherited implementations of kivy.uix.screenmanager Screen    
"""

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

#################
# Local libraries
#################
from logutils import verbose_log
from hashutils import open_and_hash_file
from filechooser import FileChooser

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
        self._content = FileChooser(
            cancel=lambda: self._popup.dismiss,
            path=FileChooser.path,
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

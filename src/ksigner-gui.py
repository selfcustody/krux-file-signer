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
ksigner-gui.py

A simple Graphical User Interface built with kivy
"""
####################
# Standard libraries
####################
import os

#######################
# Third party libraries
#######################
from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty

#################
# Local libraries
#################
from logutils import verbose_log
from hashutils import open_and_hash_file


class MainScreen(Screen):
    """
    MainScreen

    Class to manage the two main buttons:

    - Sign;
    - Verify;
    """

    def on_press_sign_button(self):
        """
        on_press_sign_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        verbose_log("INFO", "<MainScreen:@Button::sign> clicked")
        self.ids.main_screen_sign_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_sign_button(self):
        """
        on_release_sign_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to SignScreen
        """
        verbose_log("INFO", "<MainScreen@Button::sign> released")
        self.ids.main_screen_sign_button.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "left"
        self.manager.current = "sign"

    def on_press_verify_button(self):
        """
        on_press_verify_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        verbose_log("INFO", "<MainScreen:@Button::verify> clicked")
        self.ids.main_screen_verify_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_verify_button(self):
        """
        on_release_verify_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to VerifyScreen
        """
        verbose_log("INFO", "<MainScreen:@Button::verify> released")
        self.ids.main_screen_verify_button.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "left"
        self.manager.current = "verify"


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


class VerifyScreen(Screen):
    """
    VerifyScreen
    
    Is a sub-widget, managed by KSignerApp@ScreenManager
    that executes signature verifications    
    """
    pass


class KSignerApp(App):
    """
    KSignerApp is the Root widget
    """
    
    def build(self):
        """
        build

        Create the Root widget with an ScreenManager
        as manager for its sub-widgets:

        - main;
        - sign;
        - verify;
        - TODO: others
        """
        # Create the screen manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name="main"))
        screen_manager.add_widget(SignScreen(name="sign"))
        screen_manager.add_widget(VerifyScreen(name="verify"))
        return screen_manager


if __name__ == "__main__":
    app = KSignerApp()
    app.run()

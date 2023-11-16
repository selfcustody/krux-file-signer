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
import os
from pathlib import Path

#######################
# Third party libraries
#######################
from kivy.uix.screenmanager import ScreenManager
from kivy.cache import Cache
from kivy.core.text import LabelBase
from kivysome.iconfonts import register

#################
# Local libraries
#################
from cli.getsome import info
from screens.main import MainScreen
from screens.sign import SignScreen
from screens.verify import VerifyScreen
from screens.qrcode import QRCodeScreen
from screens.scan import ScanScreen
from loggedapp import LoggedApp

class KSignerApp(LoggedApp):
    """
    KSignerApp is the Root widget
    """
        
    def _register_font(self, **kwargs):
        """
        Register a font located at :path:`fonts`
        """
        font_name = kwargs.get("font_name")
        root_path = Path(__file__).parent.parent.absolute()
        font_path = str(root_path / "fonts" / f"{font_name}.ttf")
        msg = f"{info()}: Registering font '{font_name}' at {font_path}"
        self.debug(msg)

        if font_name.startswith("fa"):
            fontd_path = str(root_path / "fonts" / f"{font_name}.fontd")
            register(font_name, font_path, fontd_path)
        else:
            LabelBase.register(name=font_name, fn_regular=font_path)

    def _register_cacher(self):
        cache_name = "ksigner"
        cache_args = {"limit": 10, "timeout": 300}
        Cache.register(cache_name, **cache_args)

    def _register_screens(self) -> ScreenManager:
        screen_manager = ScreenManager()
        screens = (
            MainScreen(name="main"),
            SignScreen(name="sign"),
            VerifyScreen(name="verify"),
            QRCodeScreen(name="export-sha256"),
            ScanScreen(name="import-signature"),
            ScanScreen(name="import-public-key"),
        )

        for screen in screens:
            msg = f"{info()}: adding screen '{screen.name}'"
            self.debug(msg)
            screen_manager.add_widget(screen)

        return screen_manager

    def build(self):
        """
        Create the Root widget with an ScreenManager
        as manager for its sub-widgets:
        """
        self._register_font(font_name="terminus")
        self._register_font(font_name="fa-regular-6.4.2")
        self._register_cacher()
        return self._register_screens()


if __name__ == "__main__":
    app = KSignerApp()
    app.run()

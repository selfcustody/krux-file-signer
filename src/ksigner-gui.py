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

#######################
# Third party libraries
#######################
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivy.cache import Cache
from kivy.core.text import LabelBase

#################
# Local libraries
#################
from cli.getsome import info
from screens.main import MainScreen
from screens.sign import SignScreen
from screens.verify import VerifyScreen
from screens.qrcode import QRCodeScreen
from screens.scan import ScanScreen


class KSignerApp(App):
    """
    KSignerApp is the Root widget
    """

    def _register_font(self):
        """
        Register 'terminus' font
        """
        _font_name = "terminus"
        _dirname = os.path.dirname(__file__)
        _terminus_path = os.path.join(_dirname, "terminus.ttf")
        _absdir = os.path.abspath(_terminus_path)
        
        msg = "%s: Registering font '%s' at %s" % (info(), "terminus", _absdir)
        Logger.warning(msg)
        LabelBase.register(name=_font_name, fn_regular=_absdir)
    
    def _register_cacher(self):
        cache_name = "ksigner"
        cache_args = { "limit": 10, "timeout": 300 }
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
            msg = "%s: adding screen '%s'" % (info(), screen.name)
            Logger.debug(msg)
            screen_manager.add_widget(screen)
            
        return screen_manager
    
    def build(self):
        """
        Create the Root widget with an ScreenManager
        as manager for its sub-widgets:
        """
        msg = "%s: %s" % (info(), "Starting ksigner")
        Logger.info(msg)

        self._register_cacher()
        self._register_font()
        return self._register_screens()


if __name__ == "__main__":    
    app = KSignerApp()
    app.run()

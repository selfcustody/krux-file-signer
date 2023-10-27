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
        cache_name = "ksigner"
        cache_args = { "limit": 10, "timeout": 300 }
        
        Cache.register(cache_name, **cache_args)

        msg = "%s: %s" % (info(), "Starting ksigner")
        Logger.info(msg)
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


if __name__ == "__main__":
    app = KSignerApp()
    app.run()

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
#################
# Local libraries
#################
from screens.logscreen import LoggedScreen


class VerifyScreen(LoggedScreen):
    """
    VerifyScreen

    Is a sub-widget, managed by KSignerApp@ScreenManager
    that executes signature verifications

    - [x] Load file
    - [x] Load signature
    - Load publickey
    - Verify signature
    """

    def on_press_verify_screen_load_file_button(self):
        """
        on_press_verify_screen_load_file_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        self.log.info("<MainScreen:@Button::verify> clicked")
        self.ids.verify_screen_load_file_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_verify_screen_load_file_button(self):
        """
        on_release_verify_screen_load_file_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to SignScreen
        """
        self.log.info("<MainScreen@Button::sign> released")
        self.ids.verify_screen_load_file_button.background_color = (0, 0, 0, 0)

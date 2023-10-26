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
mainscreen.py

Implements an inherited screens.logscreen.LoggedScreen
"""

#################
# Local libraries
#################
from screens.actioner import ActionerScreen
# pylint: disable=no-name-in-module
from kivy.properties import StringProperty, ListProperty

class MainScreen(ActionerScreen):
    """
    MainScreen

    Class to manage :mod:`screens` :class:`screens.SignScreen` and
    :class:`screens.VerifyScreen`.
    """

    name = StringProperty("main")
         
    def on_press_sign_button(self):
        """
        on_press_sign_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        self._on_press(id="main_screen_sign_button")

    def on_release_sign_button(self):
        """
        on_release_sign_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to SignScreen
        """
        self._on_release(id="main_screen_sign_button")
        self._set_transition(direction="left")
        self._set_current(screen="sign")

    def on_press_verify_button(self):
        """
        on_press_verify_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        self._on_press(id="main_screen_verify_button")
        
    def on_release_verify_button(self):
        """
        on_release_verify_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to VerifyScreen
        """
        self._on_release(id="main_screen_verify_button")
        self._set_transition(direction="left")
        self._set_current(screen="verify")

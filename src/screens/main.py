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

Implements an inherited kivy.uix.screenmanager.Screen
"""

#######################
# Third party libraries
#######################
from kivy.uix.screenmanager import Screen

#################
# Local libraries
#################
from utils.log import logger


class MainScreen(Screen):
    """
    MainScreen

    Class to manage :mod:`screens` :class:`screens.SignScreen` and
    :class:`screens.VerifyScreen`.
    """

    def on_press_sign_button(self):
        """
        on_press_sign_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        logger("DEBUG", "MainScreen: <Button::sign> clicked")
        self.ids.main_screen_sign_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_sign_button(self):
        """
        on_release_sign_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to SignScreen
        """
        logger("DEBUG", "MainScreen: <Button::sign> released")
        self.ids.main_screen_sign_button.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "left"
        self.manager.current = "sign"

    def on_press_verify_button(self):
        """
        on_press_verify_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        logger("DEBUG", "MainScreen: <Button::verify> clicked")
        self.ids.main_screen_verify_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_verify_button(self):
        """
        on_release_verify_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to VerifyScreen
        """
        logger("DEBUG", "MainScreen: <Button::verify> released")
        self.ids.main_screen_verify_button.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "left"
        self.manager.current = "verify"

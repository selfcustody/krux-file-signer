
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
logscreen.py

Implements an inherited kivy.uix.screenmanager.Screen
with inner logger. Use it as super class
"""

#######################
# Third party libraries
#######################
from kivy.uix.screenmanager import Screen

#################
# Local libraries
#################
from utils.log import build_logger


class LoggedScreen(Screen):
    """
    MainScreen

    Class to manage :mod:`screens` :class:`screens.SignScreen` and
    :class:`screens.VerifyScreen`.
    """

    def __init__(self, **kwargs):
        self.loglevel = kwargs.pop("loglevel")
        super().__init__(**kwargs)
        self.log = build_logger(__name__, self.loglevel)

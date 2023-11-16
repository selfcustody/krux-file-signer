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
####################
# Standard libraries
####################
import os

#######################
# Third party libraries
#######################
from kivy.logger import Logger, LOG_LEVELS

#################
# Local libraries
#################
from cli.getsome import info


class KLogger:
    """
    KLogger

    Class to manage logger on kivy classes
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.environ.get("LOG_LEVEL"):
            self.loglevel = LOG_LEVELS[os.environ["LOG_LEVEL"]]
        else:
            self.loglevel = LOG_LEVELS["info"]
        Logger.setLevel(self.loglevel)

    def _create_msg(self, msg):
        """
        Create the logged message with current
        class caller
        """
        return f"{info()}: {msg}"

    def info(self, msg):
        """
        Create the info message with the current
        class caller
        """
        Logger.info(self._create_msg(msg))

    def debug(self, msg):
        """
        Create the debug message with the current
        class caller
        """
        Logger.debug(self._create_msg(msg))

    def warning(self, msg):
        """
        Create the warning message with the current
        class caller
        """
        Logger.warning(self._create_msg(msg))

    def error(self, msg):
        """
        Create the error message with the current
        class caller
        """
        Logger.error(self._create_msg(msg))

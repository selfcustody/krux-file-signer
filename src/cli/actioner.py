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
actioner.py

Implements an abstract class with the kivy.logger.Logger
to be used with Signer and Verifyer
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


class Actioner:
    """
    Base class for Signer and Verifyer
    """

    def __init__(self):
        if os.environ.get("LOG_LEVEL"):
            _loglevel = LOG_LEVELS[os.environ["LOG_LEVEL"]]
        else:
            _loglevel = LOG_LEVELS["info"]
        Logger.setLevel(_loglevel)

    def info(self, msg):
        """
        Logger with info level
        """
        Logger.info("%s: %s", info().strip(), msg)

    def debug(self, msg):
        """
        Logger with debug level
        """
        Logger.debug("%s: %s", info().strip(), msg)

    def warning(self, msg):
        """
        Logger with warning level
        """
        Logger.warning("%s: %s", info().strip(), msg)

    def error(self, msg):
        """
        Logger with error level
        """
        Logger.error("%s: %s", info().strip(), msg)

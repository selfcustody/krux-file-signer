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
signscreen.py

An inherited implementations of kivy.uix.screenmanager Screen    
"""
####################
# Standard libraries
####################
import os

#####################
# Thirparty libraries
#####################
from kivy.logger import Logger, LOG_LEVELS
from kivy.cache import Cache


class LoggedCache:
    """
    Class to joint :class:`Cache` with :class:`Logger`
    features
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.environ.get("LOG_LEVEL"):
            loglevel = LOG_LEVELS[os.environ["LOG_LEVEL"]]
        else:
            loglevel = LOG_LEVELS["info"]
        Logger.setLevel(loglevel)

    @staticmethod
    def register(name, **kwargs):
        """
        Do the same as :method:`register` from :class:`Cache`,
        with logs
        """
        dicts = dict(kwargs)
        msg = f"LoggedCache: '{name}' setup: {dicts}"
        Logger.debug(msg)
        Cache.register(name, **kwargs)
        msg = f"LoggedCache: '{name}' registered"
        Logger.info(msg)

    @staticmethod
    def append(reg, key, value):
        """
        Append a mapped key:value in register cache
        and log its
        """
        msg = f"LoggedCache: Saving {reg}->{key}={value}"
        Logger.debug(msg)
        Cache.append(reg, key, value)

    @staticmethod
    def get(reg, key):
        """
        Get a mapped key:value in register cache
        and log its
        """
        _value = Cache.get(reg, key)
        msg = f"LoggedCache: Getting {reg}->{key}={_value}"
        Logger.debug(msg)
        return _value

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

A simple Graphical User Interface version
of ksigner-cli.py based o tkinter.

TODO: rebuild to kivy?    
"""

####################
# Standard libraries
####################
import os
import base64
import argparse

#######################
# Third party libraries
#######################
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class MainPage(GridLayout): pass
class SignPage(GridLayout): pass
class VerifyPage(GridLayout): pass

class KSignerApp(App):

    PAGE = 'Main'
     
    def build(self):

        if (KSignerApp.PAGE == 'Main'):
            return MainPage()
        elif (KSignerApp.PAGE == 'Sign'):
            return SignPage()
        elif (KSignerPAGE == 'Verify'):
            return VerifyPage()

                   
if __name__ == '__main__':
    app = KSignerApp()
    app.run()
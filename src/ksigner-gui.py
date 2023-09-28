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
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class KSignerWidget(Widget):
    pass

class KSignerApp(App):
    
    def build(self):

        self.current_page = 'Main'
        
        if (self.current_page == 'Main'):        
            btn = Button(
                text ="Scan sha256 hash",
                font_size ="20sp",
                background_color =(0, 0, 0, 0),
                color =(1, 1, 1, 1),
                size_hint =(.2, .2),
                pos =(300, 250)
            )
 
            # bind() use to bind the button to function callback
            btn.bind(on_press = self.scan_sha256_hash_callback)
            return btn

    def scan_sha256_hash_callback(self, event):
        self.current_page = 'Scanning'
        print("changed")

                   
if __name__ == '__main__':
    app = KSignerApp()
    app.run()
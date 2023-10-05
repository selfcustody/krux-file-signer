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
qrcodescreen.py

Implements an inherited kivy.uix.screenmanager.Screen
for display QRCodes    
"""

##################
# Standard library
##################
import time

#######################
# Third party libraries
#######################
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

#################
# Local libraries
#################
from logutils import verbose_log

COLOR_BLACK = (0, 0, 0, 1)
COLOR_WHITE = (1, 1, 1, 1)
QRCODE_VERSION = 1
BOX_SIZE = 10
BORDER_SIZE = 4

class QRCodeScreen(Screen):
    """
    Class responsible to display qrcodes.
    It's an custom clone from
    https://github.com/odudex/krux/blob/android/android/mocks/lcd_mock.py
    """      
    code = StringProperty('')
    text = StringProperty('')
        

    def on_pre_enter(self):
        """
        Event fired when the screen is about to be used: the entering animation is started.
        """
        self.generate_label()
        self.generate_qrcode()
        
    def on_enter(self):
        """
        Event fired when the screen is displayed: the entering animation is complete.
        """
        pass
    
    def generate_label(self):
        verbose_log("INFO", "Creating <QRCodeScreen@Label>")
        label = Label(
            text=self.text,
            font_size=self.height // 5,
            font_name='terminus.ttf',
            halign='center',
            color=COLOR_WHITE,
            markup=True
        )        
        self.add_widget(label)

    def generate_qrcode(self):
        verbose_log("INFO", "Creating QRCode")
        qrcode = QRCode(
            version=QRCODE_VERSION,
            error_correction=ERROR_CORRECT_L,
            box_size=BOX_SIZE,
            border=BORDER_SIZE
        )
        verbose_log("INFO", qrcode)

        verbose_log("INFO", "Adding data")
        qrcode.add_data(self.code)
        
        verbose_log("INFO", "Creating <QRCodeScreen@Image>")
        qrcode.make(fit=True)
        self.img = qrcode.make_image(fill_color="black", back_color="white")


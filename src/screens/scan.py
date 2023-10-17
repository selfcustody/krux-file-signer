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
scan.py

Implements an inherited kivy.uix.screenmanager.Screen
for scan QRCodes
"""

################
# Kivy libraries
################
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    ObjectProperty,
)
from kivy_garden.zbarcam import ZBarCam
from pyzbar.pyzbar import ZBarSymbol

#################
# Local libraries
#################
from utils.log import logger


class ScanScreen(Screen):
    """
    Class responsible to scan qrcodes.
    """
    
    fill_color = ListProperty((1, 1, 1, 1))
    """
    :data:`background_color` is a tuple describing the color of background
    defined at :class:`~qrcode.QRCode`
    """
        
    label_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.125})
    """
    :data:`label_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    zbar_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.5})
    """
    :data:`label_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """
    
    warn_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 1})
    """
    :data:`warn_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #Widgets
        self._label_warn = None 
        self._label_desc = None
        self._box_layout = None
        self._zbarcam = None

        # Keyboard bindings for close ScanScreen
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            logger("WARNING", "QRCodeScreen: This widget is a VKeyboard object")
            # which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_pre_enter(self, *args):
        """
        Event fired when the screen is about to be used: the entering animation is started.
        """
        self.set_box_layout()
        self.set_label_warn()
        self.set_zbarcam()
        self.set_label_desc()
        
    def set_box_layout(self):
        """
        Sets and add BoxLayout Widget that wrap
        all needed widgets
        """
        self._box_layout = BoxLayout(orientation="vertical")
        self.add_widget(self._box_layout)
        logger("DEBUG", "ScanScreen: <BoxLayout> added")
    
    def set_label_warn(self):
        """
        Sets and add Label Widget that warn user about
        the what to do on ScanScreen
        """
        if self.manager.current == "scan-import-save-signature":
            text = "\n".join([
                "(a) Scan the signed message;",
                "(b) click on scren or press one of 'esc|enter|backspace|left button' to proceed"
            ])
        elif self.manager.current == "scan-import-save-public-key":
            text = "\n".join([
                "(a) Scan the hexadecimal public key;",
                "(b) click on scren or press one of 'esc|enter|backspace|left button' to proceed"
            ])
        else:
            raise Exception(f"Invalid screen: {self.manager.current}")
            
        self._label_warn = Label(
            text=text,
            font_size=Window.height // 35,
            font_name="terminus.ttf",
            halign="center",
            color=self.fill_color,
            markup=True
        )
        logger("INFO", "ScanScreen: <Label::warning> added to <BoxLayout>")
        self._box_layout.add_widget(self._label_warn)
        
    def set_zbarcam(self):
        """
        Sets and add ZBarCam Widget that describe the qrcode's
        data to ScanScreen
        """
        self._zbarcam = ZBarCam()
        self._box_layout.add_widget(self._zbarcam)
        logger("INFO", "ScanScreen: <ZBarCam> added to <BoxLayout>")
        Clock.schedule_interval(self._decode_qrcode, 1)
        
    def set_label_desc(self):
        """
        Sets and add Label Widget that describe the qrcode's
        data to ScanScreen
        """

        if self.manager.current == "scan-import-save-signature":
            text = "Signed message: ",
        elif self.manager.current == "scan-import-save-public-key":
            text = "Public key: "
        else:
            raise Exception(f"Invalid screen: {self.manager.current}")
        
        self._label_desc = Label(
            text=text,
            font_size=Window.height // 50,
            font_name="terminus.ttf",
            halign="center",
            color=self.fill_color,
            markup=True,
            pos_hint=self.label_pos_hint,
        )
        self._box_layout.add_widget(self._label_desc)
        logger("INFO", "ScanScreen: <Label::description> added to <BoxLayout>")

    def _back_to_signscreen(self):
        """
        Back to SignScreen
        """
        logger("DEBUG", "ScanScreen: Redirecting to <SignScreen>")
        self.manager.transition.direction = "left"
        self.manager.current = "sign"
        
    def _keyboard_closed(self):
        logger("WARNING", "ScanScreen: keyboard have been closed")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            self._back_to_signscreen()

        elif keycode[1] == 'enter':
            self._back_to_signscreen()

        elif keycode[1] == 'left':
            self._back_to_signscreen()

        elif keycode[1] == 'backspace':
            self._back_to_signscreen()
        else:
            logger("WARNING", f"ScanScreen: key '{keycode[1]}' not implemented")

        return True

    @staticmethod
    def _chunk_str(msg, size):
        """
        Split a big string in multiple lines;
        Use with sha256 or signature strings.
        """
        if (not msg):
            return "None"
        else:
            return "\n".join([
                msg[i:i+size] for i in range(0, len(msg), size)
            ])
        
    def _decode_qrcode(self, *args):
        """
        When camera capture the QRCode,
        :data:`zbarcam.symbols` will be filled;
        When it occurs, stop scanning

        @see https://stackoverflow.com/questions/73067952/kivy-load-camera-zbarscan-on-click-button/73077097#73077097
        """
        logger("DEBUG", "ScanScreen: waiting for qrcode")
        if len(self._zbarcam.symbols) > 0:
            scanned_data = self._zbarcam.symbols[0].data.decode("UTF-8")
            self._label_desc += ScanScreen._chunk_str(scanned_data, 12)
            
            logger("DEBUG", f"ScanScreen: captured '{scanned_data}'")
            Clock.unschedule(self._decode_qrcode, 1)
            self._zbarcam.stop() # stop zbarcam
            self._zbarcam.ids['xcamera']._camera._device.release()        
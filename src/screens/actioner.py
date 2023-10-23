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

Implements an inherited kivy.uix.screenmanager.Screen
to be subclassed on qrcody.py and scan.py
"""

################
# Kivy libraries
################
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import ListProperty, ObjectProperty

#################
# Local libraries
#################
from screens.logscreen import LoggedScreen

class ActionerScreen(LoggedScreen):
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

    warn_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 1})
    """
    :data:`warn_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Widgets
        self._label_warn = None
        self._label_desc = None
        
        # Keyboard bindings for close ScanScreen
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        if self._keyboard.widget:
            self.log.warning("ActionerScreen: This widget is a VKeyboard object")
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _make_label_warn(self, text):
        return Label(
            text=text,
            font_size=Window.height // 35,
            font_name="terminus.ttf",
            halign="center",
            color=self.fill_color,
            markup=True,
            pos_hint=self.warn_pos_hint,
        )

    def _make_label_desc(self, text):
        return Label(
            text=text,
            font_size=Window.height // 35,
            font_name="terminus.ttf",
            halign="center",
            color=self.fill_color,
            markup=True,
            pos_hint=self.label_pos_hint,
        )

    def _back_to_signscreen(self):
        """
        Back to SignScreen
        """
        self.log.info("ActionerScreen: Redirecting to <SignScreen>")
        self.manager.transition.direction = "left"
        self.manager.current = "sign"

    def _keyboard_closed(self):
        self.log.info("ActionerScreen: keyboard have been closed")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    # pylint: disable=unused-argument
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == "escape":
            self._back_to_signscreen()

        elif keycode[1] == "enter":
            self._back_to_signscreen()

        elif keycode[1] == "left":
            self._back_to_signscreen()

        elif keycode[1] == "backspace":
            self._back_to_signscreen()
        else:
            self.log.warning("ActionerScreen: key '%s' not implemented", keycode[1])

        return True

    @staticmethod
    def _chunk_str(msg, size):
        """
        Split a big string in multiple lines;
        Use with sha256 or signature strings.
        """
        return "\n".join([msg[i : i + size] for i in range(0, len(msg), size)])

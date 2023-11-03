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

    warn_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.9})
    """
    :data:`warn_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    base_label_kwargs = {
        "font_size": Window.height // 35,
        "font_name": "terminus",
        "halign": "center",
        "markup": True,
    }
    """
    Base **kargs for for Labels 
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Widgets
        self._label_warn = None
        self._label_desc = None

        # Keyboard bindings for close ScanScreen
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _set_background(self, **kwargs):
        name = kwargs.get("name")
        _id = kwargs.get("id")
        red = kwargs.get("r")
        green = kwargs.get("g")
        blue = kwargs.get("b")
        alpha = kwargs.get("a")

        # Log first
        msg = f"<Button::{name}> {_id}.background_color=({red},{green},{blue},{alpha})"
        self.debug(msg)

        # set after
        widget = self.ids[id]
        widget.background_color = (red, green, blue, alpha)

    def _set_screen(self, **kwargs):
        """
        Change to some screen registered on
        screenmanager.

        Kwargs:
        -------
            :param:`name` of registered screen
            :param:`direction` of transiction
        """
        name = kwargs.get("name")
        direction = kwargs.get("direction")
        print(self.manager.screen_names)

        msg = f"Switching to screen='{name}' by direction='{direction}'"
        self.debug(msg)
        self.manager.transition.direction = direction
        self.manager.current = name

    def _on_press(self, **kwargs):
        """
        General on_press method to change
        background of buttons, based on
        id of widget

        Kwargs:
        -------
            :param:`id` the kivy id of widget
        """
        _id = kwargs.get("id")
        msg = f"<Button::{_id}> clicked"
        self.info(msg)
        self._set_background(name=self.name, id=id, r=0.5, g=0.5, b=0.5, a=0.5)

    def _on_release(self, **kwargs):
        """
        General on_release method to change
        background of buttons and redirection
        of actions, based on id of widget

        Kwargs:
        -------
            :param:`id` the kivy id of widget
        """
        _id = kwargs.get("id")
        msg = f"<Button::{_id}> released"
        self.info(msg)
        self._set_background(name=self.name, id=_id, r=0, b=0, g=0, a=0)

    def _make_label(self, **kwargs):
        """
        Build a label

        Kwargs:
        -------
            :param text
            :param type can be 'description' or 'warning'
        """

        _text = kwargs.get("text")
        _type = kwargs.get("type")
        msg = f"building '{_type}' label='{_text}'"
        self.debug(msg)
        __kwargs__ = self.base_label_kwargs
        __kwargs__["text"] = _text
        __kwargs__["color"] = self.fill_color

        if _type == "description":
            __kwargs__["pos_hint"] = self.label_pos_hint

        elif _type == "warning":
            __kwargs__["pos_hint"] = self.warn_pos_hint

        else:
            msg = f"Invalid type '{_type}'"
            raise ValueError(msg)

        msg = "label args: %s" % __kwargs__
        self.debug(msg)
        return Label(**__kwargs__)

    def _keyboard_closed(self):
        self.debug("closing keyboard")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    # pylint: disable=unused-argument
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        # for key in ["escape"]
        if keycode[1] == "enter":
            msg = f"{keycode[1]} pressed"
            if self.manager.current == "sign":
                self._set_screen(name="main", direction="left")
            elif self.manager.current == "export-sha256":
                self._set_screen(name="sign", direction="left")
            elif self.manager.current == "import-signature":
                self._set_screen(name="sign", direction="left")
            elif self.manager.current == "import-public-key":
                self._set_screen(name="sign", direction="left")
            else:
                msg = f"key '{keycode[1]}' isnt implemented"
                self.warning(msg)
        return True

    def _chunk_str(self, msg, size):
        """
        Split a big string in multiple lines;
        Use with sha256 or signature strings.
        """

        _msg = f"chunking {msg} to substrings with len={size}"
        self.debug(_msg)
        return "\n".join([msg[i : i + size] for i in range(0, len(msg), size)])

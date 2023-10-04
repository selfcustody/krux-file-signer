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
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.label import CoreLabel
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.graphics import Rotate
from kivy.clock import mainthread


COLOR_BLACK = (0, 0, 0, 1)
COLOR_WHITE = (1, 1, 1, 1)

class QRCodeScreen(Screen):
    """
    Class responsible to display qrcodes.
    It's an custom clone from
    https://github.com/odudex/krux/blob/android/android/mocks/lcd_mock.py
    """      
    file_input = StringProperty('')
    #file_hash = StringProperty(None)
    #file_raw_hash = StringProperty(None)

class QRCodeWidget(Widget):
    
    pressed = ListProperty([0, 0])
    released = ListProperty([0, 0])
    
    def __init__(self, **kwargs):
        super(QRCodeWidget, self).__init__(**kwargs)
        self.landscape = False
        self.frame_counter = 0
        _, window_height = Window.size
        self.font_size = window_height // 25

    def rgb565torgb111(self, color):
        """convert from gggbbbbbrrrrrggg to tuple"""
        MASK5 = 0b11111
        MASK3 = 0b111

        red = ((color >> 3) & MASK5)
        red /= 31
        green = color >> 13
        green += (color & MASK3) << 3
        green /= 63
        blue = ((color >> 8) & MASK5)
        blue /= 31
        return (red, green, blue, 1)

    @mainthread
    def clear(self, color):
        color = self.rgb565torgb111(color)
        Window.clearcolor = color
        self.canvas.clear()

    @mainthread
    def rotation(self, r):
        if r == 2:
            with self.canvas:
                # PushMatrix()
                Rotate(origin=self.center, angle=-90)
                # PopMatrix()
            self.landscape = True
        else:
            with self.canvas:
                # PushMatrix()
                Rotate(origin=self.center, angle=90)
                # PopMatrix()
            self.landscape = False
        time.sleep(0.01)
 

    def _width(self):
        return int(self.width)

    def _height(self):
        if self.height > 200:
            return int(self.height)
        # widget size not ready at boot, so gets window size
        _, window_height = Window.size
        return window_height
    
    @mainthread
    def draw_qr_code(self, offset_y, code_str, max_width, dark_color=COLOR_BLACK, light_color=COLOR_WHITE, bg_color=COLOR_BLACK):
        dark_color = self.rgb565torgb111(dark_color)
        light_color = self.rgb565torgb111(light_color)
        starting_size = 2
        while code_str[starting_size] != "\n":
            starting_size += 1
        # starting size is the amount of blocks per line
        max_width = min(self._width(), self._height())
        # scale is how many pixels per block
        scale = max_width // starting_size
        # qr_width is total QR width in pixels
        qr_width = starting_size * scale
        #texture = Texture.create(size=(starting_size, starting_size), colorfmt='rgb')
        texture = Texture.create(size=(starting_size, starting_size), colorfmt='rgb')
        # buf_size = starting_size * starting_size
        buf_size = starting_size * starting_size
        buf_size *= 3
        buf = [0 for x in range(buf_size)]
        pixel_index = 0
        for inverted_y in range(starting_size): # vertical blocks loop
            y = starting_size - inverted_y - 1
            for x in range(starting_size): # horizontal blocks loop
                xy_index = y * (starting_size+1) + x  # individual block index
                color = dark_color if code_str[xy_index] == "1" else light_color
                if isinstance(color, int):
                    color = int(str(color),16)
                    red = color//256
                    green = red
                    blue = red
                else:
                    red, green, blue, _ = color
                    red *= 255
                    green *= 255
                    blue *= 255
                buf[pixel_index*3] = int(red)
                buf[pixel_index*3+1] = int(green)
                buf[pixel_index*3+2] = int(blue)
                pixel_index += 1
        # offset will be used only in position for Android
        offset = (max_width - qr_width) // 2      
        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.mag_filter = 'nearest'

        with self.canvas:
            Rectangle(
                texture=texture,
                pos=(offset + 0, self._height() - offset - qr_width),
                size=(starting_size*scale, starting_size*scale)
            )
        
    @mainthread
    def display(self, img, oft=None, roi=None):
        return
        self.frame_counter += 1
        self.draw_string(50,50, str(self.frame_counter))
        frame = img.get_frame()
        if not isinstance(frame, MagicMock):
            buf = frame.tostring()/enc
            image_texture = Texture.create(
                size=(self._width(), self._height()),
                colorfmt='bgr'
            )
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture
            with self.canvas:
                Rectangle(texture=image_texture, pos=self.pos, size=(self._width(), self._height()))

    def on_touch_down(self, touch):
        x, y = touch.pos
        y = self._height() - y
        if self.pressed == ([x, y]):
            x +=1 #force event if touches in same place as before
        self.pressed = ([x, y])
        return True

    def on_touch_up(self, touch):
        x, y = touch.pos
        y = self._height() - y
        if self.released == ([x, y]):
            x +=1 #force event if touches in same place as before
        self.released = ([x, y])
        return True

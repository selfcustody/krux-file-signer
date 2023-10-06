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
from threading import Thread

#######################
# Third party libraries
#######################
from functools import partial
from qrcode import QRCode

################
# Kivy libraries
################
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from qrcode.constants import ERROR_CORRECT_L
from kivy.uix.label import Label

from kivy.uix.screenmanager import Screen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty
)

#################
# Local libraries
#################
from logutils import verbose_log

COLOR_WHITE = (1, 1, 1, 1)

class QRCodeScreen(Screen):
    """
    Class responsible to display qrcodes.
    It's an custom clone from
    https://github.com/odudex/krux/blob/android/android/mocks/lcd_mock.py
    """ 
     
    code = StringProperty('')
    """
    The string code to be parsed on QRCode.        
    """
    
    text = StringProperty('')
    """
    The label to be show describing the QRCode
    """
    
    version = NumericProperty(1)
    """
    The QRCode version. GO from 1 to 40.
    """
    
    ecc = NumericProperty(ERROR_CORRECT_L)
    """
    The error correction code level for the qrcode.

    :data:`ecc` is the Error Correrction Code level.
    The default value is a constant in :module:`~qrcode.constants`,
    defaulting to `qrcode.constants.ERROR_CORRECT_L`.
    """

    box_size = 10
    """
    Size of box
    """

    border_size = 3
    """
    Size of border
    """

    background_color = ListProperty((0, 0, 0, 1))
    """
    :data:`color_black` is a tuple describing the background
    """

    loading_image = StringProperty('data/images/image-loading.gif')
    """Intermediate image to be displayed while the widget ios being loaded.

    :data:`loading_image` is a :class:`~kivy.properties.StringProperty`,
    defaulting to `'data/images/image-loading.gif'`.
    """


    def __init__(self, **kwargs):
        super(QRCodeScreen, self).__init__(**kwargs)
        self._label = None
        self._qrcode = None
        self._qrtexture = None
        self._image = None

    def on_data(self, instance, value):
        if not (self.canvas or value):
            return

        if not self._img:
            # if texture hasn't yet been created delay the texture updating
            Clock.schedule_once(lambda dt: self._on_data(instance, value))
            return
        self._img.anim_delay = .25
        self._img.source = self.loading_image
        
    def on_pre_enter(self):
        """
        Event fired when the screen is about to be used: the entering animation is started.
        """
        self.set_image()
        self.set_label()   
        Thread(target=partial(self.generate_qrcode)).start()
        
    def on_enter(self):
        """
        Event fired when the screen is displayed: the entering animation is complete.
        """
        pass

    def set_image(self):
        """
        Sets and add Image Widget to QRCodeScreen
        """
        verbose_log("INFO", "Creating <QRCodeScreen@Image")
        self._img = Image(
            pos_hint={'center_x': .5, 'center_y': .5},
            allow_stretch=True,
            size_hint=(None, None),
            size=(self.width * .9, self.height * .9)
        )
        self.add_widget(self._img)
        
    def set_label(self):
        """
        Sets and add Label Widget to QRCodeScreen
        """
        verbose_log("INFO", "Creating <QRCodeScreen@Label>")
        self._label = Label(
            text=self.text,
            font_size=self.height // 5,
            font_name='terminus.ttf',
            halign='center',
            color=COLOR_WHITE,
            markup=True
        )        
        self.add_widget(self._label)

    def generate_qrcode(self):
        """
        Setup QRCode
        """
        try:
            verbose_log("INFO", "Creating QRCode")
            self._qrcode = QRCode(
                version=self.version,
                error_correction=self.ecc,
                box_size=self.box_size,
                border=self.border_size
            )

            verbose_log("INFO", "Adding data")
            self._qrcode.add_data(self.code)
        
            verbose_log("INFO", "Creating <QRCodeScreen@Image>")
            self._qrcode.make(fit=True)
        except Exception as e:
            verbose_log("ERROR", e)
            self._qrcode = None
        finally:
            self._update_texture()

    def _create_texture(self, k, dt):
        verbose_log("INFO", "Setting <QRCodeScreen@Texture>")
        self._qrtexture = texture = Texture.create(size=(k, k), colorfmt='rgb')
        # don't interpolate texture
        texture.min_filter = 'nearest'
        texture.mag_filter = 'nearest'

    def _update_texture(self):
        verbose_log("INFO", "Updating <QRCodeScreen@Texture>")
        matrix = self._qrcode.get_matrix()
        k = len(matrix)

        # create the texture in main UI thread otherwise
        # this will lead to memory corruption
        verbose_log("INFO", "Creating <QRCodeScreen@Texture> in mainUI Thread")
        Clock.schedule_once(partial(self._create_texture, k), -1)

        cr, cg, cb, ca = self.background_color[:]
        cr, cg, cb = int(cr*255), int(cg*255), int(cb*255)
        # used bytearray for python 3.5 eliminates need for btext
        buff = bytearray()
        for r in range(k):
            for c in range(k):
                buff.extend([0, 0, 0] if matrix[r][c] else [cr, cg, cb])

        # then blit the buffer
        # join not necessary when using a byte array
        # buff =''.join(map(chr, buff))
        # update texture in UI thread.
        verbose_log("INFO", "Blitting buffer in <QRCodeScreen@Texture>")
        Clock.schedule_once(lambda dt: self._upd_texture(buff))

    def _upd_texture(self, buff):
        texture = self._qrtexture
    
        if not texture:
            verbose_log("WARN", "Texture hasn't been created")
            Clock.schedule_once(lambda dt: self._upd_texture(buff))
            return

        verbose_log("INFO", "Setup image texture")
        texture.blit_buffer(
            buff,
            colorfmt='rgb',
            bufferfmt='ubyte'
        )
        texture.flip_vertical()
        self._img.anim_delay = -1
        self._img.texture = texture
        self._img.canvas.ask_update()

    


"""
verifyscreen.py

Implements an inhrited kivy.uix.screenmanager.Screen
"""

######################
# Thirdparty libraries
######################
from kivy.uix.screenmanager import Screen

#################
# Local libraries
#################
from logutils import verbose_log

class VerifyScreen(Screen):
    """
    VerifyScreen
    
    Is a sub-widget, managed by KSignerApp@ScreenManager
    that executes signature verifications
    
    - [x] Load file
    - [x] Load signature
    - Load publickey
    - Verify signature
    """

    def on_press_verify_screen_load_file_button(self):
        """
        on_press_verify_screen_load_file_button
        
        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        verbose_log("INFO", "<MainScreen:@Button::verify> clicked")
        self.ids.verify_screen_load_file_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_verify_screen_load_file_button(self):
        """
        on_release_verify_screen_load_file_button
        
        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to SignScreen
        """
        verbose_log("INFO", "<MainScreen@Button::sign> released")
        self.ids.verify_screen_load_file_button.background_color = (0, 0, 0, 0)

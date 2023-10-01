"""
mainscreen.py

Implements an inherited kivy.uix.screenmanager.Screen
"""

#######################
# Third party libraries
#######################
from kivy.uix.screenmanager import Screen

#################
# Local libraries
#################
from logutils import verbose_log


class MainScreen(Screen):
    """
    MainScreen

    Class to manage the two main buttons:

    - Sign;
    - Verify;
    """

    def on_press_sign_button(self):
        """
        on_press_sign_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        verbose_log("INFO", "<MainScreen:@Button::sign> clicked")
        self.ids.main_screen_sign_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_sign_button(self):
        """
        on_release_sign_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to SignScreen
        """
        verbose_log("INFO", "<MainScreen@Button::sign> released")
        self.ids.main_screen_sign_button.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "left"
        self.manager.current = "sign"

    def on_press_verify_button(self):
        """
        on_press_verify_button

        - change background color of button to (.5,.5,.5,.5),
          giving a visual effect of 'pressed'
        """
        verbose_log("INFO", "<MainScreen:@Button::verify> clicked")
        self.ids.main_screen_verify_button.background_color = (0.5, 0.5, 0.5, 0.5)

    def on_release_verify_button(self):
        """
        on_release_verify_button

        - change background color of button to (0, 0, 0, 0),
          giving a visual effect of 'unpressed'
        - make a screen transition to VerifyScreen
        """
        verbose_log("INFO", "<MainScreen:@Button::verify> released")
        self.ids.main_screen_verify_button.background_color = (0, 0, 0, 0)
        self.manager.transition.direction = "left"
        self.manager.current = "verify"

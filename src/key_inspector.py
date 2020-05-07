"""

    Affiche interactive - inspecteur de clavier
        Idée Originale: Damien Muti
        Code : Olivier Boesch

"""

# ----- kivy config
from kivy.config import Config
# don't stop app on escape (should I?)
# Config.set('kivy', 'exit_on_escape', 0)

# try to set width and height to 400x200
# doesn't work on pi since all kv app are fullscreen with the egl_rpi window provider
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

# force cursor display (useful on pi)
Config.set('modules', 'cursor', '1')

# kivy imports
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.logger import Logger


class KeyboardController(Widget):
    """KeyboardController: class to get keypress"""
    def __init__(self, app, **kwargs):
        """__init__:
            args:
                app: reference to main app"""
        self.app = app
        # call parent class init
        super().__init__(**kwargs)
        # request keyboard and bind keypress (down) to keyboard_callback
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_callback)

    def _keyboard_closed(self):
        """_keyboard_closed: restores thing when leaving keyboard """
        self._keyboard.unbind(on_key_down=self.keyboard_callback)
        self._keyboard = None

    def keyboard_callback(self, keyboard, keycode, text, modifiers):
        """keyboard_callback: callback called on each keypress
        to get key code"""
        # get the label by its id and set its text with the keycode
        self.app.root.ids['display_lbl'].text = "key: \""+keycode[1]+"\""
        Logger.info("Key pressed: {} {} {}".format(str(keycode), str(text), str(modifiers)))

# UI for this app
kv_str = """
BoxLayout:
    orientation: 'vertical'
    Label:
        id : display_lbl
        font_size: sp(15)
    Button:
        size_hint_y: None
        height: dp(40)
        text: 'Quit'
        # when we release the button -> stop the app
        on_release: app.stop()
"""


class KeyInspectorApp(App):
    """KeyInspectorApp: main app class"""

    # title of the window
    title = 'Key Inspector'
    # a future ref for the controller
    keyboard_controller = None

    def build(self):
        """build: builds the ui"""
        # create an set the keyboard controller
        self.keyboard_controller = KeyboardController(self)
        # load the ui string and get the root widget
        root = Builder.load_string(kv_str)
        # return the root to the app
        return root

    def _on_keyboard_settings(self, window, *largs):
        """overridden function to prevent F1 key from displaying settings"""
        pass


# if this file is the main file -> launch the app
if __name__ == '__main__':
    KeyInspectorApp().run()

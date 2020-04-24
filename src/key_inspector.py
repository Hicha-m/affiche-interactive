"""

    Affiche interactive
        Idée Originale: Damien Muti
        Code : Olivier Boesch

"""

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.logger import Logger


class KeyboardController(Widget):
    def __init__(self, app, **kwargs):
        self.app = app
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_callback)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.keyboard_callback)
        self._keyboard = None

    def keyboard_callback(self, keyboard, keycode, text, modifiers):
        self.app.root.ids['display_lbl'].text = "key: \""+keycode[1]+"\""
        Logger.info("Key pressed: {} {} {}".format(str(keycode), str(text), str(modifiers)))


kv_str = """
BoxLayout:
    orientation: 'vertical'
    Label:
        id : display_lbl
    Button:
        size_hint_y: None
        height: dp(40)
        text: 'Quit'
        on_release: app.stop()
"""


class KeyInspectorApp(App):

    title = 'Key Inspector'

    def build(self):
        self.keyboard_controller = KeyboardController(self)
        root = Builder.load_string(kv_str)
        return root


if __name__ == '__main__':
    KeyInspectorApp().run()

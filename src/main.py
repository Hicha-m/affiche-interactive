"""

    Affiche interactive 
        Idée Originale: Damien Muti
        Code : Olivier Boesch

"""

import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
os.environ["KIVY_AUDIO"] = "sdl2"  # workaround for gstreamer bug on rpi3

from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")
Config.set("graphics", "show_cursor", "0")

import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.logger import Logger


class MediaManager(Widget):
    def __init__(self, config_file=None, **kwargs):
        super().__init__(**kwargs)
        self.load_file(config_file)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_callback)
        config = {}
        self.sound = None
        self.video = None
        self.image = None
        
    def load_file(self, src=None):
        if src is None:
            src = 'media/config.json'
        try:
            Logger.info("Media Config: Loading file {}".format(src))
            with open(src, 'r') as f:
                data = f.read()
            self.config = json.loads(data)
            Logger.info("Media Config: Config Loaded -> {}".format(str(self.config)))
        except Exception as e:
            raise e
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.keyboard_callback)
        self._keyboard = None
    
    def keyboard_callback(self, keyboard, keycode, text, modifiers):
        Logger.info("Keyboard: Pressed {}".format(str(keycode)))
        media = self.config.get(keycode[1], None)
        Logger.info("Media: found {}".format(str(media)))
        if media is None:
            return
        if not os.path.exists(media['src']):
            Logger.warning("Media: file not found {}".format(str(media)))
            return
        if media['media_type'] == 'video':
            if self.screen_manager.current == 'image':
                self.image.clear_image()    
            self.screen_manager.current = 'video'
            self.video.change_media(media)
        elif media['media_type'] == 'image':
            if self.screen_manager.current == 'video':
                self.video.stop_media()
            self.screen_manager.current = 'image'
            self.image.change_media(media)
        elif media['media_type'] == 'sound':
            src = os.path.join(os.getcwd(), media['src'])
            if self.sound is None:
                self.sound = SoundLoader.load(src)
                if self.sound:
                    self.sound.play()
            else:
                if self.sound.source != src:
                    self.sound.stop()
                    self.sound = SoundLoader.load(src)
                    if self.sound:
                        self.sound.play()
                elif self.sound.state == 'play':
                    self.sound.stop()
                else:
                    self.sound.play()
            

class VideoScreen(Screen):
    def get_video_widget(self):
        return self.ids['video_widget']
        
    def change_media(self, media):
        src = os.path.join(os.getcwd(), media['src'])
        wid = self.get_video_widget()
        if wid.source != src:
            wid.source = src
            wid.state = 'play'
        elif wid.state == 'play':
            wid.seek(0)
            wid.state = 'stop'
        else:
            wid.seek(0)
            wid.state = 'play'
        
    def stop_media(self):
        wid = self.get_video_widget()
        wid.seek(0)
        wid.state = 'stop'
        

class ImageScreen(Screen):
    def get_image_widget(self):
        return self.ids['image_widget']
        
    def change_media(self, media):
        src = os.path.join(os.getcwd(), media['src'])
        wid = self.get_image_widget()
        if wid.source != src:
            wid.source = src
        else:
            wid.source = ""

    def clear_image(self):
        image = self.get_image_widget()
        image.source = ""


Builder.load_file('afficheinteractive.kv')


class AfficheApp(App):

    def build(self):
        self.media_manager = MediaManager()
        video_screen = VideoScreen(name='video')
        image_screen = ImageScreen(name='image')
        self.media_manager.video = video_screen
        self.media_manager.image = image_screen
        sm = ScreenManager(transition=NoTransition())
        self.media_manager.screen_manager = sm
        sm.add_widget(image_screen)
        sm.add_widget(video_screen)
        return sm


if __name__ == '__main__':
    AfficheApp().run()

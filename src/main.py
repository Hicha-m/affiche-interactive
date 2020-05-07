"""

    Affiche interactive 
        Idée Originale: Damien Muti
        Code : Olivier Boesch

"""

__version__ = '0.9'

# Kivy : set providers for audio and video
# with env vars
import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
os.environ["KIVY_AUDIO"] = "sdl2"  # workaround for gstreamer bug on rpi3

# Kivy : set specific config
# app fullscreen and don't show cursor
from kivy.config import Config
# Config.set("graphics", "fullscreen", "auto")
Config.set("graphics", "show_cursor", "0")

# kivy imports
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.logger import Logger


class MediaManager(Widget):
    """Media Manager: capture each keypress,
    lookup in config for medium attached to this key, switch on the right screen
    and transmit medium path to image or video widgets. Plays audio directly"""
    def __init__(self, config_file=None, **kwargs):
        """Class init"""
        super().__init__(**kwargs)
        self.config = {}
        self.load_config_file(config_file)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_callback)
        self.sound = None
        self.video = None
        self.image = None
        
    def load_config_file(self, src=None):
        """load_config_file: loads a configuration file for the app that links key to media
            arguments:
                src : filename of config file (defaults to 'config.json')
            format of the file :
            {
                "key1": {"media_type": "video",  "src": "media/videoname.mp4"},
                "key2": {"media_type": "image",  "src": "media/imagename.jpg"},
                "key3": {"media_type": "sound",  "src": "media/soundname.mp3"}
            }
            correct key names can be found with the key inspector app
        """
        # if a name if not provided -> defaults to config.json in the media dir
        if src is None:
            src = 'media/config.json'
        try:
            # open and load file
            Logger.info("Media Config: Loading file {}".format(src))
            with open(src, 'r') as f:
                data = f.read()
            # decode json and store dict
            self.config = json.loads(data)
            Logger.info("Media Config: Config Loaded -> {}".format(str(self.config)))
        # if we can't load config -> no need to continue : raise exception
        except Exception as e:
            raise e
    
    def _keyboard_closed(self):
        """_keyboard_closed: unbind callback when keyboard is closed"""
        self._keyboard.unbind(on_key_down=self.keyboard_callback)
        self._keyboard = None
    
    def keyboard_callback(self, keyboard, keycode, text, modifiers):
        """keyboard_callback: get keypress and try to find media accordingly"""
        # which key ?
        Logger.info("Keyboard: Pressed {}".format(str(keycode)))
        # try to get the right medium in config
        media = self.config.get(keycode[1], None)
        Logger.info("Media: found {}".format(str(media)))
        # no medium -> finished
        if media is None:
            return
        # medium found in config but not on disk -> warning
        if not os.path.exists(media['src']):
            Logger.warning("Media: file not found {}".format(str(media)))
            return
        # medium found is a video
        if media['media_type'] == 'video':
            # clear if an image is displayed
            if self.screen_manager.current == 'image':
                self.image.clear_image()
            # switch to video screen
            self.screen_manager.current = 'video'
            # give medium path to the video screen
            self.video.change_media(media)
        # medium found is an image
        elif media['media_type'] == 'image':
            # stop if a video is displayed
            if self.screen_manager.current == 'video':
                self.video.stop_media()
            # switch to image screen
            self.screen_manager.current = 'image'
            # give medium path to the image screen
            self.image.change_media(media)
        # medium found is a sound
        elif media['media_type'] == 'sound':
            # get absolute path
            src = os.path.join(os.getcwd(), media['src'])
            # if no sound was loaded -> try load it directly
            if self.sound is None:
                self.sound = SoundLoader.load(src)
                # if it is loaded -> play it
                if self.sound:
                    self.sound.play()
            # there was already a sound loaded
            else:
                # if it's not the same -> stop it, try load the new one then play it
                if self.sound.source != src:
                    self.sound.stop()
                    self.sound = SoundLoader.load(src)
                    if self.sound:
                        self.sound.play()
                # it's the same as before -> toggle state play/pause
                elif self.sound.state == 'play':
                    self.sound.stop()
                else:
                    self.sound.play()
            

class VideoScreen(Screen):
    """VideoScreen: display videos"""
    # TODO: make seek correctly work as play after stop doesn't show the image (no rewind)
    def get_video_widget(self):
        """get_video_widget: return video widget"""
        return self.ids['video_widget']
        
    def change_media(self, media):
        """change_media: change media source to new one or toggle state of the current one
            args :
                media : current medium relative path to the app directory"""
        # get absolute path
        src = os.path.join(os.getcwd(), media['src'])
        # get video widget
        wid = self.get_video_widget()
        # if it's not the same -> load and play
        if wid.source != src:
            wid.source = src
            wid.state = 'play'
        # it's the same -> toggle state play/stop
        elif wid.state == 'play':
            # rewind video before pause
            wid.seek(0)
            wid.state = 'stop'
        else:
            wid.state = 'play'
        
    def stop_media(self):
        """stop_media : rewind and stop current media"""
        wid = self.get_video_widget()
        wid.seek(0)
        wid.state = 'stop'
        

class ImageScreen(Screen):
    """ImageScreen: display images"""
    def get_image_widget(self):
        """get_image_widget: return image widget"""
        return self.ids['image_widget']
        
    def change_media(self, media):
        """change_media: change media source to new one or toggle state of the current one
            args :
                media : current medium relative path to the app directory"""
        # get absolute path to media
        src = os.path.join(os.getcwd(), media['src'])
        # get image widget
        wid = self.get_image_widget()
        # if the source changed -> load the new one
        if wid.source != src:
            wid.source = src
        # else -> set screen to black (no source)
        else:
            wid.source = ""

    def clear_image(self):
        """clear_image: clear image to have a black screen"""
        # get image widget
        image = self.get_image_widget()
        # unset source to obtain a black screen
        image.source = ""


# Load the kv file
# note : this could be set automatically if the kv file is named affiche.kv
# (because the app is named AFFICHEApp)
Builder.load_file('afficheinteractive.kv')


class AfficheApp(App):
    """AfficheApp: main application class"""

    def build(self):
        """build: setup of the ui"""
        # create the media manager
        self.media_manager = MediaManager()
        # create video and image screens
        video_screen = VideoScreen(name='video')
        image_screen = ImageScreen(name='image')
        # set a reference of the screens in the media manager
        self.media_manager.video = video_screen
        self.media_manager.image = image_screen
        # create the screen manager
        sm = ScreenManager(transition=NoTransition())
        # add the two screens to the screen manager
        sm.add_widget(image_screen)
        sm.add_widget(video_screen)
        # set a reference of the screen manager in the media manager
        self.media_manager.screen_manager = sm
        # return the root widget for display
        return sm

    def _on_keyboard_settings(self, window, *largs):
        """overridden function to prevent F1 key from displaying settings"""
        pass


# if this file is the main file -> launch the app
if __name__ == '__main__':
    AfficheApp().run()

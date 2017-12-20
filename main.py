from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config

from gui.main_menu import MainMenu
from gui.results import Results

Config.set('graphics', 'multisamples', '0')


class OCRApp(App):
    def __init__(self, **kwargs):
        super(OCRApp, self).__init__(**kwargs)
        self.main_menu = MainMenu(name='menu')
        self.results = Results(name='results')
        self.main_menu.bind(on_ocr_run=self.append_images)

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(self.main_menu)
        self.root.add_widget(self.results)
        return self.root

    def append_images(self, instance, images, api_key):
        self.results.api_key = api_key
        self.results.image_filenames = images


if __name__ == '__main__':
    OCRApp().run()

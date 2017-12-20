from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import glob

from kivy.uix.togglebutton import ToggleButton


class MainMenu(Screen):
    def __init__(self, **kwargs):
        self._on_ocr_run_name = 'on_ocr_run'
        self.register_event_type(self._on_ocr_run_name)
        super(MainMenu, self).__init__(**kwargs)
        self.file_path = TextInput(size_hint_x=5, text="C:\\Users\\f.jawien\\PycharmProjects\\EngineeringProject\\ocr")
        self.api_key_input = TextInput(size_hint_y=1, text='AIzaSyDvTxaEcTkZTxCeNfLqdUExql - ldhbl4I4')
        self.images_viewer = GridLayout(cols=3, size_hint_y=6)
        self.add_widget(self.generate_content())

    def generate_content(self):
        container = BoxLayout(orientation='horizontal')

        file_path_container = BoxLayout(orientation='horizontal', size_hint_y=1, spacing=20)
        apply_path = Button(text='Load images', font_size=20, size_hint_x=2)
        apply_path.bind(on_release=self.fill_images_viewer)
        file_path_container.add_widget(self.file_path)
        file_path_container.add_widget(apply_path)

        self.fill_images_viewer()
        images_container = BoxLayout(orientation='vertical', size_hint_x=6)
        images_container.add_widget(file_path_container)
        images_container.add_widget(self.images_viewer)

        settings_container = BoxLayout(orientation='vertical', size_hint_x=4, spacing=20, padding=[20, 0, 0, 0])
        run_btn = Button(text='Run OCR', size_hint_y=6, font_size=40, background_color=[1, .3, .3, 1])
        run_btn.bind(on_press=self.run_btn_pressed, on_release=self.run_btn_pressed)
        settings_container.add_widget(self.api_key_input)
        settings_container.add_widget(run_btn)

        container.add_widget(images_container)
        container.add_widget(settings_container)
        return container

    def fill_images_viewer(self, *args):
        self.images_viewer.clear_widgets()
        image_list = self.load_images_from_file(self.file_path.text)
        for image in image_list:
            btn = Button(background_color=[0, 0, 0, 0], id=image)
            btn.bind(on_release=self.image_pressed)
            btn.bind(pos=self.apply_image, size=self.apply_image)
            self.images_viewer.add_widget(btn)

    def load_images_from_file(self, path):
        image_list = []
        for filename in glob.glob(path + '/*.jpg'):
            image_list.append(filename)

        for filename in glob.glob(path + '/*.png'):
            image_list.append(filename)

        return image_list

    def image_pressed(self, instance, *args):
        if instance.background_color == [0, 0, 0, 0]:
            instance.background_color = [0, 0, 0, .5]
        else:
            instance.background_color = [0, 0, 0, 0]
        self.apply_image(instance)

    def apply_image(self, instance, *args):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Rectangle(source=instance.id, pos=instance.pos, size=instance.size)
            if instance.background_color == [0, 0, 0, .5]:
                Rectangle(size=[50, 50], pos=[instance.x + 30, instance.y + 30], source='Icons/check.png')

    def run_btn_pressed(self, instance):
        images_to_process = []

        for image in self.images_viewer.children:
            if image.background_color == [0, 0, 0, 0.5]:
                images_to_process.append(image.id)
        self.dispatch(self._on_ocr_run_name, images_to_process, self.api_key_input.text)
        if instance.background_color == [1, .3, .3, 1]:
            instance.background_color = [1, .3, .3, .5]
        else:
            instance.background_color = [1, .3, .3, 1]
            self.manager.current = 'results'

    def on_ocr_run(self, *args):
        pass

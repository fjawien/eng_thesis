from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView


class ErrorPopup(ModalView):
    def __init__(self, message='', **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.message = message
        self.add_widget(self.generate_content())

    def generate_content(self):
        container = BoxLayout(orientation='vertical')
        text = Label(text=self.message, size_hint_y=6, font_size=25)
        btn = Button(text='OK', font_size=30)
        btn.bind(on_release=self.ok_pressed)
        container.add_widget(text)
        container.add_widget(btn)
        return container

    def ok_pressed(self, *args):
        self.dismiss()

import json
from os.path import join, basename

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from gui.error_popup import ErrorPopup
from ocr.nie_wiem import OCR

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'


class Results(Screen):
    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)
        self.api_key = ''
        self.image_filenames = ['']
        self.results_text = Label(text='aaaaa', size_hint_y=6)
        self.bind(on_pre_enter=self.run_ocr)
        self.add_widget(self.generate_content())

    def generate_content(self):
        container = BoxLayout(orientation='vertical')
        # container.bind(pos=self.color_background, size=self.color_background)
        return_btn = Button(text='Return')
        return_btn.bind(on_release=self.go_back)

        container.add_widget(self.results_text)
        container.add_widget(return_btn)
        return container

    def go_back(self, *args):
        self.manager.current = 'menu'

    def run_ocr(self, *args):
        if self.api_key:
            api_key = self.api_key
        else:
            popup = ErrorPopup('API key cannot be empty')
            popup.open()
        if self.api_key:
            image_filenames = self.image_filenames
        else:
            popup = ErrorPopup('No image chosen')
            popup.open()
        try:
            ocr_instance = OCR(api_key=api_key, image_filenames=image_filenames)
            response = ocr_instance.request_ocr()
            if response.status_code != 200 or response.json().get('error'):
                print(response.text)
            else:
                for idx, resp in enumerate(response.json()['responses']):
                    # save to JSON file
                    imgname = image_filenames[idx]
                    jpath = join(RESULTS_DIR, basename(imgname) + '.json')
                    with open(jpath, 'w') as f:
                        datatxt = json.dumps(resp, indent=2)
                        print("Wrote", len(datatxt), "bytes to", jpath)
                        f.write(datatxt)

                    # print the plaintext to screen for convenience
                    print("---------------------------------------------")
                    try:
                        t = resp['textAnnotations'][0]
                        print("    Bounding Polygon:")
                        print(t['boundingPoly'])
                        print("    Text:")
                        print(t['description'])
                        self.results_text.text = (t['description'])
                    except Exception as e:
                        print('Sthg wwent rong')
        except Exception as e:
            popup = ErrorPopup(str(e))
            popup.open()
            self.manager.current = 'menu'

    def color_background(self, instance, *args):
        # instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=instance.pos, size=instance.size)
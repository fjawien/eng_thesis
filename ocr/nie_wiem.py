import json
from base64 import b64encode
from os import makedirs

import requests

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)


class OCR:
    def __init__(self, api_key, image_filenames, **kwargs):
        self.api_key = api_key  # string containing api key
        self.image_filenames = image_filenames  # list with filenames

    def append_images(self):
        img_requests = []
        for imgname in self.image_filenames:
            with open(imgname, 'rb') as f:
                ctxt = b64encode(f.read()).decode()
                img_requests.append({
                        'image': {'content': ctxt},
                        'features': [{
                            'type': 'TEXT_DETECTION',
                            'maxResults': 1
                        }]
                })
        return img_requests

    def make_image_data(self):
        imgdict = self.append_images()
        return json.dumps({"requests": imgdict }).encode()

    def request_ocr(self):
        response = requests.post(ENDPOINT_URL,
                                 data=self.make_image_data(),
                                 params={'key': self.api_key},
                                 headers={'Content-Type': 'application/json'})
        return response

#
# if __name__ == '__main__':
#     api_key = 'AIzaSyDvTxaEcTkZTxCeNfLqdUExql - ldhbl4I4'
#     image_filenames = ['invoice.png']
#     ocr_instance = OCR(api_key=api_key,  image_filenames=image_filenames)
#
#     # if not api_key or not image_filenames:
#     #     print("""
#     #         Please supply an api key, then one or more image filenames
#     #
#     #         $ python cloudvisreq.py api_key image1.jpg image2.png""")
#     # else:
#
#     response = ocr_instance.request_ocr()
#     if response.status_code != 200 or response.json().get('error'):
#         print(response.text)
#     else:
#         for idx, resp in enumerate(response.json()['responses']):
#             # save to JSON file
#             imgname = image_filenames[idx]
#             jpath = join(RESULTS_DIR, basename(imgname) + '.json')
#             with open(jpath, 'w') as f:
#                 datatxt = json.dumps(resp, indent=2)
#                 print("Wrote", len(datatxt), "bytes to", jpath)
#                 f.write(datatxt)
#
#             # print the plaintext to screen for convenience
#             print("---------------------------------------------")
#             try:
#                 t = resp['textAnnotations'][0]
#                 print("    Bounding Polygon:")
#                 print(t['boundingPoly'])
#                 print("    Text:")
#                 print(t['description'])
#             except Exception as e:
#                 print('Sthg wwent rong')

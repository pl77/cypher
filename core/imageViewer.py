from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

# How to work kivy and PIL (Pillow) in Python -
# Necessary modules :
# from PIL import Image as PImage #(e.g.)
# from kivy.core.image import Image as CImage #(e.g.)
# pimg = PImage.open(path)
# ...... (resizing, cropping, etc.) ......
# data = io.BytesIO()
# pimg.save(data, 'PNG')
# pimg = None # There is no 'close' method in PIL Image module.
# data.seek(0)
# cimg = CImage(data, ext='png')
# data.flush()


class ImageViewer(App):

    def build_image(self, path):
        return Image(source=path)

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image


class ImageViewer(App):

    def build_image(self, path):
        return Image(source=path)

# based on: https://github.com/rlasko/photoManipulator/blob/master/manipulator.py

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image as Im
from kivy.core.image import ImageData
from kivy.graphics.texture import Texture
from kivy.uix.scatter import Scatter

from PIL import Image

class ImageViewer():

    def build_image(self, path):
        pilImage = Image.open(path)
        # issues with differences between kivy object and pil requires flipping the image to start
        pilImage = pilImage.transpose(Image.FLIP_TOP_BOTTOM)
        imgDatalst = list(self._img_read(pilImage))
        imgData = imgDatalst[0]
        myTex = Texture.create_from_data(imgData)
        displayImage = Im(texture=myTex)
        return displayImage

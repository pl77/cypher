from kivy.lang import Builder
from kivy.uix.label import Label

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from core.imageViewer import ImageViewer
from core.codeViewer import CodeViewer
from core.videoViewer import VideoViewer


# TODO: probar las extensiones de pygments
# TODO: works with warning: 'nef',
class Selector():
    def select_viewer(self, path):
        image_list = ('jpg', 'jpeg', 'png', 'bmp', 'dib', 'gif', 'ico', '3fr',
        'tga', 'tif', 'tiff')
        media_list = ('3gp', 'amr', 'flv', 'mkv', 'mp3', 'mp4', 'wav', '3g2',
        'aac', 'mov', 'aiff', 'au', 'avi', 'mpg', 'ogg', 'ppm', 'pgm', 'pbm')
        # Available lexers: http://pygments.org/docs/lexers/

        ext = path.split('.')[-1].lower()
        filename = path.split('/')[-1]
        lexerNotFound = ClassNotFound

        try:
            if get_lexer_for_filename(filename):
                return CodeViewer.build_code(self, path)
        except ClassNotFound:
            pass

        if ext in image_list:
            return ImageViewer.build_image(self, path)
        elif ext in media_list:
            return VideoViewer.build_video(self, path)
        else:
            content="Extension " + ext + " not supported"
            return Label(text=content, color=(1,0,0,1), font_size='20sp')

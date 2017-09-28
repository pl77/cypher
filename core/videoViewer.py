from kivy.app import App
from kivy.uix.video import Video

# TODO: agrandar la resolucion, apregar play, pause, volumen
# Para la reproduccion de un video antes de reproducir otro
class VideoViewer(App):
    def build_video(self, path):
        return Video(source=path, state='play')

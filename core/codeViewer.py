from kivy.app import App
from kivy.uix.codeinput import CodeInput
from kivy.extras.highlight import KivyLexer

from pygments.lexers import get_lexer_for_filename


class CodeViewer(App):
    def build_code(self, path):
        filename = path.split('/')[-1]
        monokai = [.152, .156, .133, 1] # monokai background color

        if filename.split('.')[-1] == 'kv':
            l = KivyLexer()
        else:
            l = get_lexer_for_filename(filename)

        code = open(path, 'r').read()

        return CodeInput(lexer=l, text=code, style_name='monokai', background_color=monokai, disabled=False)

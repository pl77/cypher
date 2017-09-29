import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ListProperty, StringProperty, OptionProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.image import ImageData
# from kivy.graphics import Rectangle, Color

from kivymd.theming import ThemeManager
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog

import os
import json

from core.selector import Selector
import mytoolbar


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = ObjectProperty(None)

class FileViewer(Screen):
    pathFile = ObjectProperty(None)

    def createViewer(self):
        # pathFile = MainApp.showPath(self)
        # boxWidget = BoxLayout()
        # boxWidget.add_widget(Selector.select_viewer(self, pathFile))
        #
        # with boxWidget.canvas:
        #     Color(1, 0, 0, 1)  # set the colour to red
        #     boxWidget.rect = Rectangle(pos=boxWidget.center,
        #                           size=(640,480))
        # self.add_widget(boxWidget)

        pathFile = MainApp.showPath(self)
        widget = Selector.select_viewer(self, pathFile)
        self.add_widget(widget)

    # taken and modified from kivy "work in progress" module to convert PIL image to kivy image
    # original API opened an ImageData object from a filepath
    # Extracted it from the coverage of the API in order to open an ImageData object from a PIlImage object
    # https://kivy.org/build/coverage/kivy_core_image_img_pil.html
    def _img_read(self, im):
        im.seek(0)
        try:
            img_ol = None
            while True:
                img_tmp = im
                if img_ol and (hasattr(im, 'dispose') and not im.dispose):
                    img_ol.paste(img_tmp, (0, 0), img_tmp)
                    img_tmp = img_ol
                img_ol = img_tmp
                yield ImageData(img_tmp.size[0], img_tmp.size[1],
                                img_tmp.mode.lower(), img_tmp.tobytes())
                im.seek(im.tell() + 1)
        except EOFError:
            pass

class MainApp(App):
    theme_cls = ThemeManager()
    title = "Cypher"

    pathFile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    autoPlay = BooleanProperty(False)
    showInfo = BooleanProperty(False)
    pathFolder = ObjectProperty(None)

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.loadConfig()
        return

    def on_enter(self, extension):
        self.loadData(extension)

    def _on_file_drop(self, window, file_path):
        MainApp.pathFile = file_path.decode("utf-8")
        filename = str(file_path)
        filename = filename.split('.')

        self.changeScreen()
        if self.showInfo == True:
            self.loadData(filename[-1][:-1])
        return

    # funciones para la carga de archivos ----------------
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, path=self.pathFolder)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        open(os.path.join(path, filename[0]))
        MainApp.pathFile = str(filename[0])
        filename = str(filename[0])
        filename = filename.split('.')

        if self.showInfo == True:
            self.loadData(filename[-1])
        self.dismiss_popup()

        self.changeScreen()
    # ----------------------------------------------------

    # TODO: eliminar la screen que se descarta
    def changeScreen(self):
        childrenList = self.root.ids.view_file.children

        if not childrenList:
            self.root.ids.scr_mngr.current = 'viewfile'
        else:
            self.root.ids.scr_mngr.current = 'loading'
            self.root.ids.view_file.remove_widget(childrenList[0])
            self.root.ids.scr_mngr.current = 'viewfile'

    #TODO: actualizar el numero de formatos: More than 200 formats supported
    def show_dialog(self, title, desc):
        '''
        Muestra el dialog de extensiones y About
        Condicion necesaria para About: title y desc deben ser iguales

        Parametros:
        title: titulo del dialog; nombre de la extension o 'About Cypher'
        desc: descripcion de la extension; en el caso de About debe ser igual a title
        '''
        text_about = ("A simple file viewer.\n"
                    "More than 200 formats supported, multiplatform and free (for ever)\n\n"
                    "Version: 0.1\n" "twitter.com/favcau\n" "favcau@gmail.com\n\n"
                    "Powered by Python + Kivy/KivyMD")

        # title: 'About Cypher' - desc: 'About Cypher'
        if title == desc:
            text_desc = text_about
        else:
            text_desc = desc

        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=text_desc,
                          size_hint_y=None,
                          valign='top',
                          markup=True)
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title=title,
                               content=content,
                               size_hint=(.8, None),
                               height=dp(400),
                               auto_dismiss=False)

        self.dialog.add_action_button("Done",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    # TODO: mejorar/optimizar
    def loadData(self, ext):
        cant = 0
        letters = ('a','b','c','d','e','f','g','h',
                    'i','j','k','l','m','n','o','p',
                    'q','r','s','t','u','v','w','x','y','z')

        if len(ext) == 0:
            return None

        if ext[0] == ".":
            ext = ext.split(".")[1]

        if ext[0] in letters:
            file_path = './data/' + ext[0] + '.json'
        else:
            file_path = './data/1.json'

        data = JsonStore(file_path)

        if data.exists(ext):
            platforms = str(data.get(ext)[2])
            platform_list = platforms.split(',')
            programs = str(data.get(ext)[3])
            programs_list = programs.split('][')
            body = "[b][color=3333ff]How to open:[/color][/b] \n\n"

            if len(platform_list) <= len(programs_list):
                cant = len(platform_list)
            else:
                cant = len(programs_list)

            for i in range(cant):
                for ch in ['[',']']:
                    if ch in programs_list[i]:
                        programs_list[i] = programs_list[i].replace(ch,"")
                body += ("[color=3333ff]" + platform_list[i] + ":[/color] " +
                        programs_list[i] + "\n\n")

            description = ("[color=3333ff]Name:[/color] " + str(data.get(ext)[0]) +
                              "\n\n" +
                              "[color=3333ff]Description:[/color] " + str(data.get(ext)[1]) +
                              "\n\n" +
                              body)

            self.show_dialog(ext, description)
        else:
            extError = ext + " not found"
            notFound = "Make sure that the file has a correct name"
            self.show_dialog(extError, notFound)

    def loadConfig(self):
        config = JsonStore('config.json')
        self.autoPlay = json.loads(config.get("autoplay")["active"])
        self.showInfo = json.loads(config.get("show_info")["active"])
        self.pathFolder = config.get("load_path")["path"]

    def setConfig(self):
        config = JsonStore('config.json')
        config.put('autoplay', active=str(self.autoPlay).lower())
        config.put('show_info', active=str(self.showInfo).lower())
        config.put('load_path', path=str(self.pathFolder))

    def showPath(self):
        return MainApp.pathFile


if __name__ == '__main__':
    MainApp().run()

# original:  gitlab.com/kivymd/KivyMD/blob/master/kivymd/toolbar.py

from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty, OptionProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.backgroundcolorbehavior import SpecificBackgroundColorBehavior
from kivymd.button import MDIconButton
from kivymd.theming import ThemableBehavior
from kivymd.elevationbehavior import RectangularElevationBehavior


class MyToolbar(ThemableBehavior, RectangularElevationBehavior,
              SpecificBackgroundColorBehavior, BoxLayout):
    left_action_items = ListProperty()
    right_action_items = ListProperty()

    title = StringProperty()
    hint = StringProperty()
    helper = StringProperty()

    md_bg_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super(MyToolbar, self).__init__(**kwargs)
        self.bind(specific_text_color=self.update_action_bar_text_colors)
        Clock.schedule_once(
            lambda x: self.on_left_action_items(0, self.left_action_items))
        Clock.schedule_once(
            lambda x: self.on_right_action_items(0,
                                                 self.right_action_items))

    def on_left_action_items(self, instance, value):
        self.update_action_bar(self.ids['left_actions'], value)

    def on_right_action_items(self, instance, value):
        self.update_action_bar(self.ids['right_actions'], value)

    def update_action_bar(self, action_bar, action_bar_items):
        action_bar.clear_widgets()
        new_width = 0
        for item in action_bar_items:
            new_width += dp(48)
            action_bar.add_widget(MDIconButton(icon=item[0],
                                               on_release=item[1],
                                               opposite_colors=True,
                                               text_color=self.specific_text_color,
                                               theme_text_color='Custom'))
        action_bar.width = new_width

    def update_action_bar_text_colors(self, instance, value):
        for child in self.ids['left_actions'].children:
            child.text_color = self.specific_text_color
        for child in self.ids['right_actions'].children:
            child.text_color = self.specific_text_color

# -*- coding: utf-8 -*-

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import datetime

class timerWidget(Widget):
    labeldatetime = ObjectProperty(None)
    buttoncount = ObjectProperty(None)

class MyApp(App):

    def buttoncount_clicked(self, src):
        self.root.labeldatetime.text = str(datetime.datetime.now())

    def build(self):
        self.root = timerWidget()
        self.root.buttoncount.bind(on_press=self.buttoncount_clicked)
        return self.root


if __name__ == '__main__':
    MyApp().run()

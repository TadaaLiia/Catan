import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import *

class Tile(Widget):
    ressource_type = "None"
    number = 5
    position = (0,0)

    def render(self):
        pass

class CatanGame(Widget):
    pass

    def update(self):
        pass

class CatanApp(App):

    def build(self):
        return CatanGame()


if __name__ == '__main__':
    CatanApp().run()
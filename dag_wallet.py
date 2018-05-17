from kivy.app import App
import kivy
#kivy.require("1.8.0")

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition


class BalanceScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


class LoginScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1

        self.add_widget(Label(text="Username:"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text="Password:"))
        self.password = TextInput(multiline=False, password=True)
        self.add_widget(self.password)

presentation = Builder.load_file("wallet.kv")


class MainApp(App):
    def build(self):
        return presentation


if __name__=="__main__":
    MainApp().run()



from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="User Name"))

        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text="password"))

        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.login_button = Button(text="Login")
        self.login_button.bind(state=self.login_pressed)
        self.add_widget(self.login_button)

    def getUserName(self):
        return self.username.text

    def login_pressed(self, inst, val):
        if val == "down":
            print(str(self.getUserName()))
            return self.getUserName()
        else:
            return None


class MyApp(App):
    def build(self):
        loginScreen = LoginScreen()
        # print(loginScreen.getUserName)
        return loginScreen

    # def


if __name__ == "__main__":
    MyApp().run()


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

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

        self.camera_button = Button(text ="camera")
        self.camera_button.bind(state=self.camera_pressed)
        self.add_widget(self.camera_button)
    def getUserName(self):
        return self.username.text
    def camera_pressed(self, inst, val):
        if val == "down":
            return CameraClick.capture
        else:
            return None
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


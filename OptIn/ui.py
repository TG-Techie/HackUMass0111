from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Canvas
from kivy.uix.screenmanager import ScreenManager, Screen

import bitmap as bitm


def do_nothing(*args, **kwargs):
    """
    Desc: Two guesses;
    arg *;
    kwarg **;
    """
    return

_nesting_stack = []
_kv_styleing = ''

def app_root(cls):
    """
    Desc: A decorator used to sure a ui_app inot the root app for the system;
    arg cls: the class to make root and run;
    """
    class AppInst(App):
        def build(self):
            return cls()
    AppInst().run()
    return cls


class ui_app(ScreenManager):
    """
    Desc: An app that contians pages and can be navigated around;
    """
    def page(self, cls):
        """
        Desc: a decorator used to signify that a specific page class is in this ui_app;
        arg cls: the page that is being added to this app;
        """
        self.add_widget(cls())
        return cls

class page(Screen):
    """
    Desc: A page that goes inside of an app, contains widgets;
    """

    @classmethod
    def widgetclass(cls, widcls):
        """
        Desc: A decorator that makes a class a widget that can go inside of pages;
        """
        class subwidcls(widcls):
            def __init__(self, *args, superior = None, **kwargs):
                super().__init__(*args, **kwargs)

                if superior == None:
                    superior = _nesting_stack.pop(0)
                superior.add_widget(self)

        @property
        def prop(supr):
            _nesting_stack.insert(0, supr)
            return subwidcls

        setattr(cls, widcls.__name__, prop)

@page.widgetclass
class ui_button(Button):

    def __init__(self, text, on_press = do_nothing, on_release = do_nothing, **kwargs):
        """
        desc: a button sub class to make things  more dynamic / nice;
        arg text: the text to be displayed on the button;
        kwarg on_press: the function called when a button is depressed;
        kwarg on_release: the function called when the button in un-pressed;
        kwargs superior: the screen/obj the button should go inside of.
                        only use when certian overwriding is needed or
                        when making unboudn button;
        """
        self._on_press = on_press
        self._on_release = on_release

        super().__init__(text = text, **kwargs)

        self.bind(state = self._update_state)


    def _update_state(self, inst, state):
        """
        Desc: internally used function for handling button presses;
        arg inst: the instance of the button;
        arg val: the state of the current button;
        """
        if state == 'down':
            self._on_press(inst)
        elif state == 'normal':
            self._on_release(inst)
        else:
            print('ERROR: other state entered!', state)

    @property
    def on_release(self):
        return self._on_release

    @property
    def on_press(self):
        return self._on_press

    @on_release.setter
    def on_release(self, func):
        self._on_release = on_release

    @on_press.setter
    def on_press(self, func):
        self._on_press = on_press

@page.widgetclass
class QR_code_view(Canvas):

    def show(self, )

from ui import ui_app, app_root, page


@app_root
class OptIn(ui_app):

    def __init__(self):
        super().__init__()

        @self.page
        class login_page(page):
            def __init__(self):
                super().__init__()
                self.ui_button('Hello!', on_press = print)

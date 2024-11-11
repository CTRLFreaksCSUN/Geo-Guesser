import flet as ft
from register_interface import register_interface

# generate sign in interface
class login_interface(ft.UserControl):
    def __init__(self, tab, page):
        super().__init__()
        self.build_login(tab, page)
        self.err_message

    # load login page
    def build_login(self, tab, screen):
        screen.window.width = 1300
        screen.window.height = 1000
        screen.window.alignment = ft.Alignment(0, 0)
        username = ft.TextField(hint_text='Enter your username', width=350, max_length=36)
        password = ft.TextField(hint_text='Enter your password', width=350, password=True, can_reveal_password=True, max_length=42)
        exit_btn = ft.ElevatedButton(text='Close app', on_click = tab.close_app)
        self.err_message = ft.Text("* Wrong username/password. Please re-enter *", color='red', visible=False)
        screen.controls.append(ft.Row([ft.Column([username, password, self.err_message, ft.ElevatedButton(
                                                                        text='Sign In', 
                                                                        on_click=lambda e: [self.confirm_login(e, username, password)]),
                                                                      ft.ElevatedButton(text='Sign Up', 
                                                                        on_click=lambda e: [register_interface(screen)])],
                                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                                        horizontal_alignment=ft.CrossAxisAlignment.START)], 
                                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                                        vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True))
        screen.add(exit_btn)
        screen.update()
    
    # verify user information
    def confirm_login(self, e, name, password):
        if(self.checkLoginIsValid(e, name, 8) and self.checkLoginIsValid(e, password, 12)):
            self.err_message.visible = False

        e.control.page.update()

    def checkLoginIsValid(self, e, cred, length):
        if (len(cred.value) >= length):
            cred.border_color = 'black'
            e.control.page.update()
            return True
        else:
            cred.border_color = 'red'
            self.err_message.visible = True
            e.control.page.update()
            return False
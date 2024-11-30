import flet as ft
import re
import pymongo
from pymongo.encryption import ClientEncryption
from KeyVaultManager import retrieveKey

# loads a register page on top of already existing login page
class register_interface(ft.UserControl):
    def __init__(self, page, client):
        super().__init__()
        self.build_register(page, client)
        self.err_message

    # creates register form     
    def build_register(self, page, client):
        new_user = ft.TextField(hint_text=' Enter new username', width=350, max_length=36)
        new_email = ft.TextField(hint_text='Enter the email you want to use', width=350, max_length=40)
        new_passw = ft.TextField(hint_text='Enter new password', width=350, password=True, can_reveal_password=True, max_length=42)
        passw_re = ft.TextField(hint_text='Re-enter new password', width=350, password=True, can_reveal_password=True, max_length=42)
        self.err_message = ft.Text("", color='red', visible=False)
        n_page = ft.Container(width=1300, height=1000, alignment=ft.alignment.center,
                                                                       content=ft.Row([ft.Column([new_user, new_email, new_passw, passw_re, self.err_message,
                                                                               ft.ElevatedButton(text='Create account',
                                                                                                 on_click=lambda e: [self.confirm_register(e, client, new_user, new_passw, passw_re, new_email)])],
                                                                                                 alignment=ft.MainAxisAlignment.CENTER,
                                                                                                 horizontal_alignment=ft.CrossAxisAlignment.START)],
                                                                                                 alignment=ft.MainAxisAlignment.CENTER,
                                                                                                 vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                                                                 expand=True))
        page.controls.append(ft.ElevatedButton(text='Back to Sign In', on_click=lambda e: [page.remove(n_page), page.remove(e.control)]))
        page.add(n_page)
        page.update()

    # verify new user information is valid
    def confirm_register(self, e, client, name, password, passw_re, email):
        if(self.checkRegisterIsValid(e, name, password, passw_re, email)):
            if (self.userCredExists(client, name) or self.userCredExists(client, email) or self.userCredExists(client, password)):
                self.err_message.value = "User credential(s) already in use. Please re-enter."
                e.control.page.update()

        else:
            try:
                accounts = client['User']
                credentials  = {
                        "Username": name.value,
                        "Email": email.value,
                        "Password": password.value
                        }

                accounts.insert_one(credentials)

            except pymongo.errors.WriteError as err:
                print(f"Failed to insert account into User: {err}")

    # check if each of the user credentials meet the requirements
    def checkRegisterIsValid(self, e, username, password, passw_re, email):
        existingInvalid = False
        name_pattern = re.compile(r'_*[a-zA-Z]+_*[0-9]*_*') 
        foundCapitalLetters = re.search('[A-Z]+', password.value)
        foundNumbers = re.search('[0-9]+', password.value)
        foundSpecialChars = re.search('[\.-_\+@?!~\*(&^)\$#%=><,|}{\[\]]+', password.value)
        email_pattern = re.compile(r'[a-zA-Z]+[\.-_\+]*@[a-zA-z-]+\.(com|org|net|gov|edu|uk|co)')

        if (self.credLengthIsValid(username, 8) and name_pattern.search(username.value) != None):
            username.border_color = 'black'
        else:
            username.border_color = 'red'
            self.err_message.value = ("Invalid username: Username must be at least 8 characters long (may also contain numbers),"
                                                         "\n\t\tmust contain at least one alphabetical character"
                                                         "\n\t\tand must not contain any special characters (#,$,%,^,etc..)."
                                                         "\n\t\tMay also contain underscores (_).")
            existingInvalid = True

        if (email_pattern.search(email.value) != None):
            email.border_color = 'black'

        else:
            email.border_color = 'red'
            self.err_message.value = "Invalid email: must follow { name }.[ com | edu | gov | co | uk | org ] format"
            existingInvalid = True

        if (self.credLengthIsValid(password, 12) and foundCapitalLetters and foundNumbers and foundSpecialChars and (password.value == passw_re.value)):
            password.border_color = 'black'
            passw_re.border_color = 'black'

        else:
            password.border_color = 'red'
            passw_re.border_color = 'red'
            self.err_message.value = ("Invalid password: Password must be at least 12 characters long,"
                                                         "\n\t\tmust contain at least one capital letter,"
                                                         "\n\t\tmust contain at least one numerical character,"
                                                         "\n\t\tand must contain at least one of the special characters (#,$,%,^,etc..).")
            existingInvalid = True

        if (existingInvalid):
            if (len(username.value) == 0 or len(password.value) == 0 or len(email.value) == 0):
                self.err_message.value = "* Please fill in empty fields *"
   
            self.err_message.visible = True
            e.control.page.update()
            return False

        self.err_message.visible = False
        return True

    # check if user credential is valid length
    def credLengthIsValid(self, cred, length):
        if (len(cred.value) >= length):
            return True
        else:
            return False

    # checks if user exists in database
    def userCredExists(self, client, cred):
        if client.find_one({" <Field Name> ": cred.value}) != None:
            cred.border_color = 'red'
            return True 
        
        return False
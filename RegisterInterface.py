from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class RegisterInterface(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Register New User')
        layout = QVBoxLayout()

        layout.addItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Username
        username_box = QHBoxLayout()
        username_box.addStretch()
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Enter new username')
        self.username.setMaximumWidth(300)
        username_box.addWidget(self.username)
        username_box.addStretch()
        layout.addLayout(username_box)

        # Email
        email_box = QHBoxLayout()
        email_box.addStretch()
        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Enter your Email')
        self.email.setMaximumWidth(300)
        email_box.addWidget(self.email)
        email_box.addStretch()
        layout.addLayout(email_box)

        # Password
        password_box = QHBoxLayout()
        password_box.addStretch()
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Enter new password')
        self.password.setMaximumWidth(300)
        self.setup_password1_field()
        password_box.addWidget(self.password)
        password_box.addStretch()
        layout.addLayout(password_box)

        # Password re-enter
        password2_box = QHBoxLayout()
        password2_box.addStretch()
        self.password_re = QLineEdit(self)
        self.password_re.setEchoMode(QLineEdit.Password)
        self.password_re.setPlaceholderText('Re-enter your password')
        self.password_re.setMaximumWidth(300)
        self.setup_password2_field()
        password2_box.addWidget(self.password_re)
        password2_box.addStretch()
        layout.addLayout(password2_box)

        # Register button
        register = QHBoxLayout()
        register.addStretch()
        register_btn = QPushButton('Create Account', self)
        register_btn.clicked.connect(self.confirm_register)
        register_btn.setMaximumWidth(300)
        register.addWidget(register_btn)
        register.addStretch()
        layout.addLayout(register)

        # Back Button
        back = QHBoxLayout()
        back.addStretch()
        back_btn = QPushButton('Back to Login', self)
        back_btn.clicked.connect(lambda: self.main_window.setCurrentIndex(0))
        back_btn.setMaximumWidth(300)
        back.addWidget(back_btn)
        back.addStretch()
        layout.addLayout(back)

        layout.addItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def setup_password1_field(self):
        self.toggle_pass_action = QAction(QIcon('eye_opened.png'), 'Show/Hide Password', self)
        self.toggle_pass_action.triggered.connect(self.toggle_password1_visibility)
        self.password.addAction(self.toggle_pass_action, QLineEdit.TrailingPosition)
        self.password.is_password_visible = False

    def setup_password2_field(self):
        self.toggle_password2_action = QAction(QIcon('eye_opened.png'), 'Show/Hide Password', self)
        self.toggle_password2_action.triggered.connect(self.toggle_password2_visibility)
        self.password_re.addAction(self.toggle_password2_action, QLineEdit.TrailingPosition)
        self.password_re.is_password_visible = False

    def toggle_password1_visibility(self):
        self.toggle_visibility(self.password, self.toggle_pass_action, 'eye_opened.png', 'eye_closed.png')

    def toggle_password2_visibility(self):
        self.toggle_visibility(self.password_re, self.toggle_password2_action, 'eye_opened.png', 'eye_closed.png')

    def toggle_visibility(self, field, action, icon_open, icon_closed):
        if field.is_password_visible:
            field.setEchoMode(QLineEdit.Password)
            field.is_password_visible = False
            action.setIcon(QIcon(icon_open))
        else:
            field.setEchoMode(QLineEdit.Normal)
            field.is_password_visible = True
            action.setIcon(QIcon(icon_closed))

    def confirm_register(self):
        # Placeholder for registration logic
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = RegisterInterface(None)
    window.show()
    app.exec_()

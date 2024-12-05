import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from DataClient import DataClient

class LoginInterface(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

        # establish database connection
        new_client = DataClient()
        connection = new_client.connect_to_client("mongodb+srv://ctrl_freaks2024:Zwh5i908Ly0yUkMt@geovisioncloud.jrl02.mongodb.net/?retryWrites=true&w=majority&appName=GeoVisionCloud")

        self.apply_stylesheet()

    def initUI(self):
        self.setWindowTitle('Login Interface')
        self.setGeometry(100, 100, 1200, 600)

        # Overall layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Title
        title_label = QLabel('GeoVision-AI')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
        main_layout.addWidget(title_label)

        # Central layout for alignment
        center_layout = QHBoxLayout()
        center_layout.addStretch(1)


        layout = QVBoxLayout()

        # Username
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Enter your username')
        layout.addWidget(self.username)

        # Password
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Enter your password')
        self.setup_password_field()
        layout.addWidget(self.password)

        # Sign in button
        sign_in_btn = QPushButton('Sign In', self)
        sign_in_btn.clicked.connect(self.signIn)
        layout.addWidget(sign_in_btn)

        #Create account button
        create_account_btn = QPushButton('Create Account', self)
        create_account_btn.clicked.connect(self.gotoRegister)
        layout.addWidget(create_account_btn)

        center_layout.addLayout(layout)
        center_layout.addStretch(1)

        main_layout.addLayout(center_layout)

        # close app button
        bottom_layout = QHBoxLayout()
        close_app_btn = QPushButton('Close App', self)
        close_app_btn.clicked.connect(self.closeApp)
        bottom_layout.addWidget(close_app_btn)
        bottom_layout.addStretch(1)

        main_layout.addLayout(bottom_layout)


        self.setLayout(main_layout)
    def setup_password_field(self):
        # Toggle visibility action
        self.toggle_pass_action = self.password.addAction(QIcon('eye_opened.png'), QLineEdit.TrailingPosition)
        self.toggle_pass_action.triggered.connect(self.toggle_password_visibility)
        self.password.is_password_visible = False

    def toggle_password_visibility(self):
        if self.password.is_password_visible:
            self.password.setEchoMode(QLineEdit.Password)
            self.password.is_password_visible = False
            self.toggle_pass_action.setIcon(QIcon('eye_opened.png'))
        else:
            self.password.setEchoMode(QLineEdit.Normal)
            self.password.is_password_visible = True
            self.toggle_pass_action.setIcon(QIcon('eye_closed.png'))
    def signIn(self):
        username = self.username.text()
        password = self.password.text()
        if username and password:
            self.main_window.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Both username and password are required.')


    def createAccount(self):
        QMessageBox.information(self, 'Create Account', 'Account creation not implemented.') # DB Shenanigans

    def closeApp(self):
        self.close()

    def apply_stylesheet(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #3e3e3e;
            color: #ffffff; /* White text color */
        }
        QLineEdit {
            background-color: #606060;
            color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        QPushButton {
            background-color: #606060;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            color: #ffffff;
            min-width: 200px; /* Consistent button width */
        }
        QPushButton:hover {
            background-color: #535353;
        }
    """)

    def gotoRegister(self):
        self.main_window.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginInterface(None)
    ex.show()
    sys.exit(app.exec_())
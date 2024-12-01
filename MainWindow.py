from LoginInterface import LoginInterface
from RegisterInterface import RegisterInterface
from HomePage import HomePage
import sys
from PyQt5.QtWidgets import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Application')
        self.setGeometry(300, 200, 1200, 600)

        self.stack = QStackedWidget(self)

        self.login_interface = LoginInterface(self)
        self.register_interface = RegisterInterface(self)
        self.HomePage = HomePage(self)

        self.stack.addWidget(self.login_interface)
        self.stack.addWidget(self.register_interface)
        self.stack.addWidget(self.HomePage)

        self.setCentralWidget(self.stack)

    def setCurrentIndex(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
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
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
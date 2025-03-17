from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

class StaticsWindow(QMainWindow):
    def __init__(self, home_window):
        super().__init__()
        loadUi("MainWindow_Statics.ui", self)
        self.home_window = home_window

        self.Back.clicked.connect(self.go_back_home)

    def go_back_home(self):
        self.close()
        self.home_window.return_to_home()

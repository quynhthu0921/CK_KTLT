import sys
from PyQt6.QtWidgets import QApplication
from LoginWindow_Ext import LoginWindow

app = QApplication(sys.argv)
home_window = LoginWindow()
home_window.show()
sys.exit(app.exec())
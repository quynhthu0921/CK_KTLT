import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from MainWindow_Home_Ext import HomeWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("LoginWindow.ui", self)

        self.pushButtonDangNhap.clicked.connect(self.handle_login)
        self.pushButtonThoat.clicked.connect(self.close)

    def handle_login(self):
        username = self.lineEditUserName.text()
        password = self.lineEditPassword.text()

        if username == "admin" and password == "123": # Kiểm tra đơn giản
            QMessageBox.information(self, "Thông báo", "Đăng nhập thành công!")
            self.open_home_window()
        else:
            QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def open_home_window(self):
        self.home_window = HomeWindow()
        self.home_window.show()
        self.hide()
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import QtCore, QtWidgets
from LogInScreen import Ui_MainWindow
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["user"]
collection = db["account"]


class UI_Ext_LogIn(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButton_DangNhap_DN.clicked.connect(self.DangNhap)
        self.pushButton_DangKy_DN.clicked.connect(self.openSignInScreen)

        # Click label
        self.label_QuenMatKhau.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label_QuenMatKhau.mousePressEvent = self.openForgetPasswordScreen

    def DangNhap(self):
        """ Xử lý chức năng đăng nhập """

        # Bắt sự kiện Enter
        self.lineEdit_TaiKhoan_DN.returnPressed.connect(self.lineEdit_MatKhau_DN.setFocus)
        self.lineEdit_MatKhau_DN.returnPressed.connect(lambda: self.pushButton_DangNhap_DN.setFocus())
        # Lấy dữ liệu
        taikhoan = self.lineEdit_TaiKhoan_DN.text().strip()
        matkhau = self.lineEdit_MatKhau_DN.text().strip()

        # Kiểm tra nhập thiếu dữ liệu
        dulieutrong = []
        if not taikhoan:
            dulieutrong.append("Số điện thoại hoặc email")
        if not matkhau:
            dulieutrong.append("Mật khẩu")

        # Hiện thông báo dữ liệu trống
        if dulieutrong:
            QMessageBox.warning(
                self.MainWindow,
                "Thiếu thông tin",
                f"Vui lòng nhập đầy đủ thông tin sau:\n- " + "\n- ".join(dulieutrong)
            )
            return

        # Kiểm tra tài khoản trong MongoDB
        user = collection.find_one({
            "$or": [
                {"sodienthoai": taikhoan, "matkhau": matkhau},
                {"email": taikhoan, "matkhau": matkhau}
            ]
        })

        if user:
            QMessageBox.information(self.MainWindow, "Thành công", "Đăng nhập thành công.")
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Tài khoản hoặc mật khẩu không đúng. Vui lòng thử lại.")
            # Nếu sai, tự động clear tài khoản, mật khẩu, con trỏ chuột về dòng tài khoản
            self.lineEdit_TaiKhoan_DN.clear()
            self.lineEdit_MatKhau_DN.clear()
            self.lineEdit_TaiKhoan_DN.setFocus()


    def openSignInScreen(self):
        """ Mở màn hình đăng ký """
        from SignInScreen_EXT import UI_Ext_SignIn
        self.signInScreen = QMainWindow()
        self.uiSignInScreen = UI_Ext_SignIn()
        self.uiSignInScreen.setupUi(self.signInScreen)
        self.signInScreen.show()
        self.MainWindow.close()

    def openForgetPasswordScreen(self, event):
        """ Mở màn hình quên mật khẩu """
        print("Đang mở màn hình quên mật khẩu")
        from ForgetPasswordScreen_EXT import UI_Ext_ForgetPassword
        self.forgetPasswordScreen = QMainWindow()
        self.uiForgetPasswordScreen = UI_Ext_ForgetPassword()
        self.uiForgetPasswordScreen.setupUi(self.forgetPasswordScreen)
        self.forgetPasswordScreen.show()  # Hiển thị cửa sổ quên mật khẩu

        self.MainWindow.close()  # Đóng cửa sổ đăng nhập



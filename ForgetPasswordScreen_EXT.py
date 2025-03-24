from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from ForgetPasswordScreen import Ui_MainWindow
from pymongo import MongoClient
import smtplib
import random
from email.mime.text import MIMEText

client = MongoClient("mongodb://localhost:27017/")
db = client["user"]
collection = db["account"]


class UI_Ext_ForgetPassword(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.pushButton_OTP.clicked.connect(self.KiemTra)
        self.pushButton_DatMatKhau.clicked.connect(self.CapNhatMatKhau)
        self.pushButton_DangKy.clicked.connect(self.openSignInScreen)

    def KiemTra(self):
        """Kiểm tra email & số điện thoại, gửi OTP nếu hợp lệ"""
        email = self.lineEdit_Email.text().strip()
        sodienthoai = self.lineEdit_SoDienThoai.text().strip()

        # Kiểm tra email, số điện thoại trong database
        user = collection.find_one({"email": email, "sodienthoai": sodienthoai})
        if not user:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Email hoặc số điện thoại không đúng!")
            return None

        otp = random.randint(100000, 999999)
        sender_email = "thuphuongdangha@gmail.com"  # Mail dùng để gửi
        sender_password = "grqu vcqo nlhe qljb"  # Password

        msg = MIMEText(f"Mã OTP của bạn là: {otp}\n\nVui lòng không chia sẻ mã với người khác!")
        msg["Subject"] = "CineSnack - Mã xác thực"
        msg["From"] = sender_email
        msg["To"] = email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()

            # Thoong báo khi gửi thành công
            collection.update_one({"email": email}, {"$set": {"otp": otp}})
            QMessageBox.information(self.MainWindow, "Thành công", "Mã OTP đã được gửi qua email!")
            return otp

        # Thông báo khi gửi thất bại
        except Exception as e:
            print("Lỗi gửi email:", e)
            QMessageBox.warning(self.MainWindow, "Lỗi", "Gửi OTP thất bại!")
            return None

    def CapNhatMatKhau(self):
        """Xác nhân OTP, nếu trùng khớp -> cập nhật mật khẩu"""
        email = self.lineEdit_Email.text().strip()
        otp_nhap = self.lineEdit_MaXacMinh.text().strip()
        matkhau_moi = self.lineEdit_MatKhauMoi.text().strip()
        xacnhan_matkhau = self.lineEdit_XacNhanMatKhau.text().strip()

        user = collection.find_one({"email": email})
        if user and "otp" in user and str(user["otp"]) == otp_nhap:
            if matkhau_moi == xacnhan_matkhau:
                collection.update_one({"email": email}, {"$set": {"matkhau": matkhau_moi}})
                QMessageBox.information(self.MainWindow, "Thành công", "Mật khẩu đã được cập nhật!")
            else:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Mật khẩu xác nhận không khớp!")
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Mã OTP không chính xác!")

    def openSignInScreen(self):
        """ Mở màn hình đăng ký """
        from SignInScreen_EXT import UI_Ext_SignIn
        self.signInScreen = QMainWindow()
        self.uiSignInScreen = UI_Ext_SignIn()
        self.uiSignInScreen.setupUi(self.signInScreen)
        self.signInScreen.show()
        self.MainWindow.close()


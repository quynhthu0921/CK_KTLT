from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from SignInScreen import Ui_MainWindow
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import re # Kiểm tra địa chỉ Email hợp lệ bằng biểu thức chính quy


client = MongoClient("mongodb://localhost:27017/")
db = client["user"]
collection = db["account"]

class UI_Ext_SignIn(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButton_DangKy.clicked.connect(self.DangKy)
        self.pushButton_DangNhap_DK.clicked.connect(self.openDangNhap)
        # self.checkBox_NhanThongBao.stateChanged.connect(self.handleCheckBox)

    def DangKy(self):
        """ Lấy dữ liệu -> Kiểm tra hợp lệ -> Lưu về MongoDB"""
        ngaymacdinh = QDate(2000, 1, 1)  # Tạo ngày 01/01/2000
        self.dateEdit_Ngay.setDate(ngaymacdinh)
        self.dateEdit_Thang.setDate(ngaymacdinh)
        self.dateEdit_Nam.setDate(ngaymacdinh)

        self.radioButton_Nam.setChecked(False)
        self.radioButton_Nu.setChecked(False)
        self.radioButton_Khac.setChecked(False)

        # Bắt sự kiện Enter
        self.lineEdit_Ten.returnPressed.connect(self.lineEdit_HoDemTen.setFocus)
        self.lineEdit_HoDemTen.returnPressed.connect(self.lineEdit_Email.setFocus)
        self.lineEdit_Email.returnPressed.connect(self.lineEdit_MatKhau_DK.setFocus)
        self.lineEdit_MatKhau_DK.returnPressed.connect(self.lineEdit_NhapLaiMatKhau.setFocus)
        self.lineEdit_NhapLaiMatKhau.returnPressed.connect(self.lineEdit_SoDienThoai.setFocus)
        self.lineEdit_SoDienThoai.returnPressed.connect(self.radioButton_Nam.setFocus)
        # Thành phố → Nút đăng ký
        self.comboBox_TinhThanhPho.activated.connect(lambda: self.pushButton_DangKy.setFocus())

        """Lấy thông tin người dùng"""
        ten = self.lineEdit_Ten.text().strip()
        hovatendem = self.lineEdit_HoDemTen.text().strip()
        email = self.lineEdit_Email.text().strip()

        # Giới tính
        if self.radioButton_Nam.isChecked():
            gioitinh = "Nam"
        elif self.radioButton_Nu.isChecked():
            gioitinh = "Nữ"
        else:
            gioitinh = "Khác"

        matkhau = self.lineEdit_MatKhau_DK.text().strip()
        nhaplaimatkhau = self.lineEdit_NhapLaiMatKhau.text().strip()
        sodienthoai = self.lineEdit_SoDienThoai.text().strip()

        # Ngày sinh
        ngay = self.dateEdit_Ngay.date().day()
        thang = self.dateEdit_Thang.date().month()
        nam = self.dateEdit_Nam.date().year()
        ngaysinh = f"{ngay:02}/{thang:02}/{nam}"

        # Thành phố
        thanhpho = self.comboBox_TinhThanhPho.currentText()

        """Kiểm tra SĐT, email có đúng định dạng không"""
        # Email (đuôi .com hoặc .edu.vn) bao gồm các số, chữ (thường/in hoa), ".", "_", "@"
        if email == r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$':
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập lại địa chỉ email đúng định dạng")

        # Số điện thoại (chỉ số, bắt đầu với "0", t 10-11 số không gồm ký tự khác)
        if sodienthoai ==  r'^0\d{9,10}$':
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập lại số điện thoại bao gồm 10-11 chữ số, không chứ ký tự khác")

        """"Kiểm tra SĐT, email có trùng với tài khoản đã được tạo hay không"""
        if collection.find_one({"email": email}):
            QMessageBox.warning(self.MainWindow, "Lỗi", "Địa chỉ email đã được đăng ký! Hãy đăng ký bằng địa chỉ email khác")
            return
        if collection.find_one({"sodienthoai": sodienthoai}):
            QMessageBox.warning(self.MainWindow, "Lỗi", "Số điện thoại đã được đăng ký! Hãy đăng ký bằng số điện thoại khác")
            return

        """Kiểm tra người dùng nhập đủ thông tin hay chưa"""
        dulieutrong = []
        if not ten:
            dulieutrong.append("Tên")
        if not hovatendem:
            dulieutrong.append("Họ và tên đệm")
        if not email:
            dulieutrong.append("Email")
        if not gioitinh:
            dulieutrong.append("Giới tính")
        if not matkhau:
            dulieutrong.append("Mật khẩu")
        if not nhaplaimatkhau:
            dulieutrong.append("Nhập lại mật khẩu")
        if not sodienthoai:
            dulieutrong.append("Số điện thoại")
        if not ngaysinh:
            dulieutrong.append("Ngày sinh")
        if not thanhpho:
            dulieutrong.append("Thành phố")

        # Hiện thông báo dữ liệu trống
        if dulieutrong:
            QMessageBox.warning(
                self.MainWindow,
                "Thiếu thông tin",
                f"Vui lòng nhập đầy đủ các thông tin sau:\n- " + "\n- ".join(dulieutrong)
            )
            return

        """Kiểm tra mật khẩu có khớp không"""
        if matkhau != nhaplaimatkhau:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Mật khẩu nhập lại không khớp! Hãy nhập lại mật khẩu")
            return

        """ Lưu thông tin vào MongoDB"""
        user_data = {
            "ten": ten,
            "hovatendem": hovatendem,
            "email": email,
            "gioitinh": gioitinh,
            "matkhau": matkhau,
            "sodienthoai": sodienthoai,
            "ngaysinh": ngaysinh,
            "thanhpho": thanhpho
        }
        try: # Chuyển sang giao diện Home nếu đăng nhập thành công
            collection.insert_one(user_data)
            QMessageBox.information(self.MainWindow, "Thành công", "Đăng ký tài khoản thành công!")
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Đăng ký không thành công! Vui lòng thử lại.")
        # self.email = email # nếu người dùng đồng ý nhận thông báo thì gửi thông báo về mail

        # Nếu checkbox nhận thông báo được chọn, gửi email thông báo
        if self.checkBox_NhanThongBao.checkState() == Qt.CheckState.Checked:
            # receive_email = self.email
            sender_email = "thuphuongdangha@gmail.com"
            sender_password = "grqu vcqo nlhe qljb"

            msg = MIMEText(f"Tài khoản CinesSnack đã được đăng ký thành công. Vui lòng không chia sẻ tài khoản cho người khác \n\nCảm ơn bạn sử dụng CineSnack!")
            msg["Subject"] = "CineSnack - Đăng ký tài khoản thành công"
            msg["From"] = "[No Reply] - CineSnack"
            msg["To"] = email

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
                server.quit()
            except Exception as e:
                print("Lỗi gửi email:", e)
                return None

    def openDangNhap(self):
        """ Chuyển qua màn hình đăng nhập """
        from LogInScreen_EXT import UI_Ext_LogIn  # Di chuyển import vào trong hàm để tránh vòng lặp
        self.logInScreen = QMainWindow()  # Tạo cửa sổ mới cho màn hình đăng nhập
        self.uiLogInScreen = UI_Ext_LogIn()  # Tạo một instance của lớp đăng nhập
        self.uiLogInScreen.setupUi(self.logInScreen)  # Cài đặt UI cho màn hình đăng nhập
        self.logInScreen.show()  # Hiển thị cửa sổ đăng nhập
        self.MainWindow.close()  # Đóng màn hình đăng ký





from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from CompletedPurchaseScreen import Ui_MainWindow
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["invoices"]
collection = db["tickets"]

class UI_Ext_ForgetPassword(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButton_NhanHoaDon.clicked.connect(self.dong_y_nhan_mail)
        self.pushButton_GuiEmail.clicked.connect(self.gui_hoa_don)

        # Ẩn lineEdit, pushButton gửi mail, nếu click pushButton muốn gửi email -> hiện
        self.lineEdit_Email.setVisible(False)
        self.pushButton_GuiEmail.setVisible(False)

    def dong_y_nhan_mail(self):
        # Click pushButton muốn gửi email -> hiện
        self.lineEdit_Email.setVisible(True)
        self.pushButton_GuiEmail.setVisible(True)

    def gui_hoa_don(self):
        email = self.lineEdit_Email.text().strip()
        invoice = collection.find_one({"email": email}, sort=[("_id", -1)])  # Lấy hóa đơn mới nhất
        if not invoice:
            self.label_Thongbao.setText("Không tìm thấy hóa đơn")

        tongtien = (invoice["sove"] * invoice["dongiave"]) + (invoice["soluongcombo"] * invoice["dongiacombo"])
        seats = ', '.join(invoice["soghe"]) if isinstance(invoice["soghe"], list) else invoice["soghe"]

        # Định dạng email
        html_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; border: 2px solid red; padding: 20px; width: 700px; margin: auto;">
            <h2 style="color: red; text-align: center;">CINESNACK</h2>
            <h3 style="color: red; text-align: center;">XÁC NHẬN ĐẶT VÉ THÀNH CÔNG</h3>
            <p><strong>Mã vé:</strong> <span style="color: red;">{invoice["_id"]}</span></p>
            <p><strong>Phim:</strong> {invoice["phim"]}</p>
            <p><strong>Suất chiếu:</strong> {invoice["suatchieu"]}</p>
            <p><strong>Rạp:</strong> {invoice["rap"]}</p>
            <p><strong>Số ghế:</strong> {seats}</p>
            <table border="1" style="width: 100%; border-collapse: collapse; text-align: center;">
                <tr style="background-color: red; color: white; height: 40px;">
                    <th style="padding: 10px;">STT</th><th style="padding: 10px;">MẶT HÀNG</th><th style="padding: 10px;">SỐ LƯỢNG</th><th style="padding: 10px;">ĐƠN GIÁ</th><th style="padding: 10px;">THÀNH TIỀN</th>
                </tr>
                <tr style="height: 40px;"><td>1</td><td>Ghế {invoice["loaighe"]}</td><td>{invoice["sove"]}</td><td>{invoice["dongiave"]}</td><td>{invoice["sove"] * invoice["dongiave"]}</td></tr>
                <tr style="height: 40px;"><td>2</td><td>Combo {invoice["combobapnuoc"]}</td><td>{invoice["soluongcombo"]}</td><td>{invoice["dongiacombo"]}</td><td>{invoice["soluongcombo"] * invoice["dongiacombo"]}</td></tr>
                <tr style="background-color: red; color: white; height: 40px;"><td colspan="4">TỔNG TIỀN (VND)</td><td>{tongtien}</td></tr>
            </table>
            <p style="text-align: center;">Cảm ơn quý khách đã đặt vé xem phim tại CineSnack. Chúc quý khách một buổi xem phim vui vẻ!</p>
        </body>
        </html>
        '''

        sender_email = "thuphuongdangha@gmail.com"
        sender_password = "grqu vcqo nlhe qljb"
        receiver_email = invoice["email"]

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ""
        msg["Subject"] = " CineSnack - Xác nhận đặt vé thành công"
        msg.attach(MIMEText(html_content, "html"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            self.label_Thongbao.setText("Hóa đơn đã được gửi về email của bạn!")
        except Exception as e:
            self.label_Thongbao.setText("Không thể gửi hóa đơn. Vui lòng thử lại sau!")




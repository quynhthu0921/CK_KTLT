# Form implementation generated from reading ui file 'CompletedPurchaseScreen.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_Backrough = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_Backrough.setGeometry(QtCore.QRect(0, 0, 1500, 900))
        self.label_Backrough.setToolTipDuration(0)
        self.label_Backrough.setLineWidth(0)
        self.label_Backrough.setMidLineWidth(-1)
        self.label_Backrough.setText("")
        self.label_Backrough.setPixmap(QtGui.QPixmap("Pictures/Backrough.png"))
        self.label_Backrough.setScaledContents(True)
        self.label_Backrough.setObjectName("label_Backrough")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 740, 300, 90))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Pictures/Logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 400, 500, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(0, 150, 1500, 80))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(490, 440, 500, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(660, 210, 180, 180))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("Pictures/Tick.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.pushButton_TrangChu = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_TrangChu.setGeometry(QtCore.QRect(360, 780, 130, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_TrangChu.setFont(font)
        self.pushButton_TrangChu.setStyleSheet("background-color: rgb(208, 0, 0);\n"
"color: rgb(217, 217, 217);")
        self.pushButton_TrangChu.setObjectName("pushButton_TrangChu")
        self.pushButton_QuayLai = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_QuayLai.setGeometry(QtCore.QRect(520, 780, 130, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_QuayLai.setFont(font)
        self.pushButton_QuayLai.setStyleSheet("background-color: rgb(208, 0, 0);\n"
"color: rgb(217, 217, 217);")
        self.pushButton_QuayLai.setObjectName("pushButton_QuayLai")
        self.pushButton_DangXuat = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_DangXuat.setGeometry(QtCore.QRect(680, 780, 130, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_DangXuat.setFont(font)
        self.pushButton_DangXuat.setObjectName("pushButton_DangXuat")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(0, 650, 1191, 80))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.pushButton_NhanHoaDon = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_NhanHoaDon.setGeometry(QtCore.QRect(580, 530, 321, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_NhanHoaDon.setFont(font)
        self.pushButton_NhanHoaDon.setObjectName("pushButton_NhanHoaDon")
        self.label_Thongbao = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_Thongbao.setGeometry(QtCore.QRect(490, 480, 500, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(False)
        self.label_Thongbao.setFont(font)
        self.label_Thongbao.setStyleSheet("color: rgb(255, 255, 0);")
        self.label_Thongbao.setText("")
        self.label_Thongbao.setObjectName("label_Thongbao")
        self.lineEdit_Email = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_Email.setGeometry(QtCore.QRect(470, 600, 441, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.lineEdit_Email.setFont(font)
        self.lineEdit_Email.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit_Email.setObjectName("lineEdit_Email")
        self.pushButton_GuiEmail = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_GuiEmail.setGeometry(QtCore.QRect(920, 600, 131, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_GuiEmail.setFont(font)
        self.pushButton_GuiEmail.setObjectName("pushButton_GuiEmail")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Bạn đã hoàn tất quy trình mua vé. "))
        self.label_5.setText(_translate("MainWindow", "ĐẶT VÉ THÀNH CÔNG"))
        self.label_3.setText(_translate("MainWindow", "Cảm ơn bạn đã sử dụng CineSnack!"))
        self.pushButton_TrangChu.setText(_translate("MainWindow", "Trang chủ"))
        self.pushButton_QuayLai.setText(_translate("MainWindow", "Quay lại"))
        self.pushButton_DangXuat.setText(_translate("MainWindow", "Đăng xuất"))
        self.label_7.setText(_translate("MainWindow", "Cảm Ơn Bạn Đã Đặt Vé Từ CineSnack"))
        self.pushButton_NhanHoaDon.setText(_translate("MainWindow", "Tôi muốn nhận hóa đơn qua email"))
        self.lineEdit_Email.setText(_translate("MainWindow", "Nhập địa chỉ email của bạn"))
        self.pushButton_GuiEmail.setText(_translate("MainWindow", "Gửi email"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

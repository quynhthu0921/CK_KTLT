from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class TheaterWindow(QMainWindow):
    def __init__(self, home_window=None):
        super().__init__()
        loadUi("MainWindow_Theater_1.ui", self)  # Load giao diện từ file .ui

        self.home_window = home_window  # Lưu tham chiếu HomeWindow
        self.collection = self.connect_mongo()  # Kết nối MongoDB

        # Gán sự kiện cho nút
        self.Update.clicked.connect(self.open_theater_2)
        self.Back.clicked.connect(self.go_back_home)

        self.load_theater_data()  # Tải dữ liệu khi mở cửa sổ

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")  # Kết nối MongoDB
            db = client["data"]  # Chọn database
            return db["theater_lst"]  # Collection chứa danh sách rạp
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_theater_data(self):
        """Tải dữ liệu rạp chiếu từ MongoDB và hiển thị lên bảng (bỏ qua rạp đã đóng cửa)"""
        theaters = list(self.collection.find(
            {"status": {"$ne": "Đóng cửa"}},  # Chỉ lấy rạp có trạng thái khác "Đóng cửa"
            {"_id": 0, "id": 1, "name": 1, "address": 1, "contact": 1, "number_of_rooms": 1, "status": 1}
        ))

        # Thiết lập số lượng dòng và cột của bảng
        self.Tab.setRowCount(len(theaters))  # Đặt số lượng dòng bằng số lượng rạp
        self.Tab.setColumnCount(6)  # Đặt số lượng cột là 6
        self.Tab.setHorizontalHeaderLabels(
            ["ID Rạp", "Tên rạp", "Địa chỉ", "Liên hệ", "Số phòng chiếu", "Trạng thái"])

        # Hiển thị dữ liệu lên bảng
        for row, theater in enumerate(theaters):
            self.Tab.setItem(row, 0, QTableWidgetItem(theater["id"]))
            self.Tab.setItem(row, 1, QTableWidgetItem(theater["name"]))
            self.Tab.setItem(row, 2, QTableWidgetItem(theater["address"]))
            self.Tab.setItem(row, 3, QTableWidgetItem(theater["contact"]))
            self.Tab.setItem(row, 4, QTableWidgetItem(str(theater["number_of_rooms"])))
            self.Tab.setItem(row, 5, QTableWidgetItem(theater["status"]))

    def open_theater_2(self):
        """Mở cửa sổ cập nhật rạp (TheaterWindow2)"""
        try:
            from MainWindow_Theater_2_Ext import TheaterWindow2
            self.theater_window2 = TheaterWindow2(self)  # Truyền tham chiếu TheaterWindow1
            self.theater_window2.show()
            self.hide()  # Ẩn cửa sổ hiện tại
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở cửa sổ Theater 2:\n{e}")

    def go_back_home(self):
        """Quay về màn hình chính"""
        self.close()
        if self.home_window:
            self.home_window.show()  # Hiển thị lại HomeWindow

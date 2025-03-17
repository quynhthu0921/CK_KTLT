from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QApplication
from PyQt6.uic import loadUi
from pymongo import MongoClient
import sys


class MovieWindow(QMainWindow):
    def __init__(self, home_window=None):  # Nhận home_window
        super().__init__()
        loadUi("MainWindow_Movie_1.ui", self)

        self.home_window = home_window  # Lưu lại tham chiếu HomeWindow

        # Gán sự kiện cho các nút
        self.Update.clicked.connect(self.open_movie_2)
        self.Back.clicked.connect(self.go_back_home)

        self.load_movie_data()  # Tải dữ liệu khi mở cửa sổ

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")  # Kết nối MongoDB
            db = client["data"]  # Chọn database
            return db["movie_lst"]  # Trả về collection
        except Exception as e:
            print(f"Lỗi kết nối MongoDB: {e}")
            return None

    def load_movie_data(self):
        """Tải dữ liệu từ MongoDB và hiển thị lên bảng (loại bỏ phim đã dừng chiếu)"""
        collection = self.connect_mongo()
        if collection is None:
            print("Không thể kết nối MongoDB.")
            return

        # Lọc dữ liệu: Chỉ lấy các phim có trạng thái khác "Dừng chiếu"
        movies = list(collection.find(
            {"status": {"$ne": "Dừng chiếu"}},  # Điều kiện lọc
            {"_id": 0, "movie_id": 1, "name": 1, "release_date": 1, "genre": 1, "status": 1, "description": 1}

        ))

        # Cấu hình bảng hiển thị
        self.Tab.setRowCount(len(movies))
        self.Tab.setColumnCount(6)
        self.Tab.setHorizontalHeaderLabels(["ID Phim","Tên Phim", "Ngày Khởi Chiếu", "Thể Loại", "Trạng Thái", "Mô tả"])

        # Hiển thị dữ liệu lên bảng
        for row, movie in enumerate(movies):
            self.Tab.setItem(row, 0, QTableWidgetItem(movie["movie_id"]))
            self.Tab.setItem(row, 1, QTableWidgetItem(movie["name"]))
            self.Tab.setItem(row, 2, QTableWidgetItem(movie["release_date"]))
            self.Tab.setItem(row, 3, QTableWidgetItem(movie["genre"]))
            self.Tab.setItem(row, 4, QTableWidgetItem(movie["status"]))
            self.Tab.setItem(row, 5, QTableWidgetItem(movie.get("description", "Không có mô tả")))

    def open_movie_2(self):
        """Chuyển sang cửa sổ MovieWindow2"""
        from MainWindow_Movie_2_Ext import MovieWindow2
        self.movie_window2 = MovieWindow2(self)
        self.movie_window2.show()
        self.hide()

    def go_back_home(self):
        """Quay về màn hình chính"""
        self.close()  # Đóng MovieWindow
        if self.home_window:  # Kiểm tra nếu có HomeWindow
            self.home_window.show()  # Hiển thị lại HomeWindow

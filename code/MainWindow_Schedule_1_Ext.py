from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QComboBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class ScheduleWindow(QMainWindow):
    def __init__(self, home_window=None):  # Nhận tham chiếu từ HomeWindow
        super().__init__()
        loadUi("MainWindow_Schedule_1.ui", self)

        self.home_window = home_window  # Lưu tham chiếu đến HomeWindow

        # Gán sự kiện cho các nút
        self.Update.clicked.connect(self.open_schedule_2)
        self.Back.clicked.connect(self.go_back_home)
        self.List.clicked.connect(self.filter_results)

        # Tải dữ liệu vào combobox từ MongoDB
        self.load_combobox_data()

        self.load_schedule_data()  # Tải dữ liệu khi mở cửa sổ

    def load_combobox_data(self):
        """Tải dữ liệu vào combobox từ MongoDB"""
        try:
            # Kết nối MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]

            # Lấy danh sách rạp có trạng thái "Hoạt động"
            theaters_collection = db["theater_lst"]
            theater_list = theaters_collection.find({"status": "Hoạt động"}, {"_id": 0, "id": 1})
            theater_ids = [theater["id"] for theater in theater_list]  # Lấy danh sách mã rạp
            self.Theater.clear()  # Xóa dữ liệu cũ trong combobox
            self.Theater.addItem("    ")  # Thêm lựa chọn "Trống" vào đầu combobox
            self.Theater.addItems(theater_ids)  # Thêm vào combobox Rạp

            # Lấy danh sách phim có trạng thái "On-air"
            movies_collection = db["movie_lst"]
            movie_list = movies_collection.find({"status": "On-air"}, {"_id": 0, "movie_id": 1})
            movie_ids = [movie["movie_id"] for movie in movie_list]  # Lấy danh sách mã phim
            self.Movie.clear()  # Xóa dữ liệu cũ trong combobox
            self.Movie.addItem("   ")  # Thêm lựa chọn "Trống" vào đầu combobox
            self.Movie.addItems(movie_ids)  # Thêm vào combobox Phim

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu từ MongoDB:\n{e}")
    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")  # Kết nối MongoDB
            db = client["data"]  # Chọn database
            return db["showtimes_lst"]  # Trả về collection showtimes_lst
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_schedule_data(self):
        """Tải dữ liệu suất chiếu từ MongoDB và hiển thị lên bảng"""
        try:
            # Kết nối MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]

            # Lấy danh sách rạp có trạng thái "Hoạt động"
            theaters_collection = db["theater_lst"]
            active_theaters = theaters_collection.find({"status": "Hoạt động"}, {"_id": 0, "id": 1})
            active_theater_ids = theaters_collection.distinct("id", {"status": "Hoạt động"})

            # Lấy danh sách phim có trạng thái "On-air"
            movies_collection = db["movie_lst"]
            on_air_movies = movies_collection.find({"status": "On-air"}, {"_id": 0, "movie_id": 1})
            on_air_movie_ids = movies_collection.distinct("movie_id", {"status": "On-air"})  # Lấy danh sách ID phim đang chiếu

            # Lấy danh sách suất chiếu từ collection showtimes_lst
            showtimes_collection = db["showtimes_lst"]
            showtime_list = list(showtimes_collection.find(
                {
                    "cinema_id": {"$in": active_theater_ids},  # Chỉ lấy suất chiếu của rạp hoạt động
                    "movie_id": {"$in": on_air_movie_ids}  # Chỉ lấy suất chiếu của phim đang chiếu
                },
                {"_id": 0, "showtime_id": 1, "cinema_id": 1, "movie_id": 1, "room_id": 1, "date": 1, "time": 1}
            ))

            # Cấu hình bảng hiển thị
            self.Tab.setRowCount(len(showtime_list))
            self.Tab.setColumnCount(6)  # Thêm cột "Phòng chiếu"
            self.Tab.setHorizontalHeaderLabels(["Mã Suất Chiếu", "Mã Rạp", "Mã Phim", "Phòng chiếu", "Ngày", "Giờ"])

            # Hiển thị dữ liệu lên bảng
            for row, showtime in enumerate(showtime_list):
                self.Tab.setItem(row, 0, QTableWidgetItem(str(showtime.get("showtime_id", ""))))
                self.Tab.setItem(row, 1, QTableWidgetItem(showtime.get("cinema_id", "")))
                self.Tab.setItem(row, 2, QTableWidgetItem(showtime.get("movie_id", "")))
                self.Tab.setItem(row, 3,
                                 QTableWidgetItem(str(showtime.get("room_id", ""))))  # Phòng chiếu (chuyển sang str)
                self.Tab.setItem(row, 4, QTableWidgetItem(showtime.get("date", "")))
                self.Tab.setItem(row, 5, QTableWidgetItem(showtime.get("time", "")))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu từ MongoDB:\n{e}")
    def open_schedule_2(self):
        """Mở cửa sổ ScheduleWindow2 để chỉnh sửa suất chiếu"""
        try:
            from MainWindow_Schedule_2_Ext import ScheduleWindow2
            self.schedule_window2 = ScheduleWindow2(self)  # Khởi tạo cửa sổ ScheduleWindow2
            self.schedule_window2.show()  # Hiển thị cửa sổ
            self.hide()  # Ẩn ScheduleWindow
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở cửa sổ Schedule 2:\n{e}")

    def go_back_home(self):
        """Quay về màn hình chính"""
        self.close()  # Đóng ScheduleWindow
        if self.home_window:  # Kiểm tra nếu có HomeWindow
            self.home_window.show()  # Hiển thị lại HomeWindow

    def filter_results(self):
        """Lọc suất chiếu theo Rạp, Phim, Ngày nhưng phải đảm bảo phim 'On-air' và rạp 'Hoạt động'."""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]

            # Lấy danh sách ID rạp đang hoạt động
            active_theater_ids = db["theater_lst"].distinct("id", {"status": "Hoạt động"})

            # Lấy danh sách ID phim đang chiếu
            on_air_movie_ids = db["movie_lst"].distinct("movie_id", {"status": "On-air"})

            # Lấy giá trị từ giao diện
            selected_theater = self.Theater.currentText().strip()
            selected_movie = self.Movie.currentText().strip()
            selected_date = self.Date.text().strip() if self.Date.text().strip() else None

            # Xây dựng điều kiện lọc (đảm bảo luôn lọc theo rạp hoạt động và phim đang chiếu)
            query = {
                "cinema_id": {"$in": active_theater_ids},  # Chỉ lấy suất chiếu của rạp hoạt động
                "movie_id": {"$in": on_air_movie_ids}  # Chỉ lấy suất chiếu của phim đang chiếu
            }

            # Thêm điều kiện từ giao diện nếu có chọn
            if selected_theater:
                query["cinema_id"] = selected_theater if selected_theater in active_theater_ids else None
            if selected_movie:
                query["movie_id"] = selected_movie if selected_movie in on_air_movie_ids else None
            if selected_date:
                query["date"] = selected_date

            # Nếu rạp hoặc phim không hợp lệ (không thuộc danh sách hợp lệ), không cần truy vấn
            if query.get("cinema_id") is None or query.get("movie_id") is None:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy suất chiếu phù hợp!")
                return

            # Truy vấn suất chiếu từ MongoDB
            showtimes_collection = db["showtimes_lst"]
            results = list(showtimes_collection.find(
                query, {"_id": 0, "showtime_id": 1, "cinema_id": 1, "movie_id": 1, "room_id": 1, "date": 1, "time": 1}
            ))

            # Kiểm tra nếu không có kết quả
            if not results:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy suất chiếu phù hợp!")
                return

            # Hiển thị dữ liệu lên bảng
            self.Tab.setRowCount(len(results))
            self.Tab.setColumnCount(6)
            self.Tab.setHorizontalHeaderLabels(["Mã Suất Chiếu", "Mã Rạp", "Mã Phim", "Phòng chiếu", "Ngày", "Giờ"])

            for row, result in enumerate(results):
                self.Tab.setItem(row, 0, QTableWidgetItem(str(result["showtime_id"])))
                self.Tab.setItem(row, 1, QTableWidgetItem(result["cinema_id"]))
                self.Tab.setItem(row, 2, QTableWidgetItem(result["movie_id"]))
                self.Tab.setItem(row, 3, QTableWidgetItem(str(result["room_id"])))  # Chuyển số thành chuỗi
                self.Tab.setItem(row, 4, QTableWidgetItem(result["date"]))
                self.Tab.setItem(row, 5, QTableWidgetItem(result["time"]))

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lọc dữ liệu:\n{e}")

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class ScheduleWindow2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("MainWindow_Schedule_2.ui", self)  # Load giao diện UI
        self.parent_window = parent  # Lưu cửa sổ cha

        # Kết nối MongoDB
        self.collection = self.connect_mongo()
        self.theaters_collection = self.connect_mongo_theaters()
        self.movies_collection = self.connect_mongo_movies()

        # Gán sự kiện cho các nút
        self.Add.clicked.connect(self.add_showtime)  # Thêm suất chiếu
        self.Fix.clicked.connect(self.fix_showtime)  # Cập nhật suất chiếu
        self.Delete.clicked.connect(self.delete_showtime)  # Xóa suất chiếu
        self.Back.clicked.connect(self.return_to_schedule1)  # Quay lại cửa sổ trước

        # Khi nhập ID suất chiếu, tự động hiển thị thông tin nếu có
        self.ID.textChanged.connect(self.load_existing_showtime)

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]  # Database name
            return db["showtimes_lst"]  # Collection name
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    @staticmethod
    def connect_mongo_theaters():
        """Kết nối MongoDB và trả về collection theaters"""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]  # Database name
            return db["theater_lst"]  # Collection name
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    @staticmethod
    def connect_mongo_movies():
        """Kết nối MongoDB và trả về collection movies"""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]  # Database name
            return db["movie_lst"]  # Collection name
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_existing_showtime(self):
        """Tự động hiển thị thông tin nếu suất chiếu đã tồn tại"""
        showtime_id = self.ID.text().strip()
        if not showtime_id:
            return

        try:
            showtime = self.collection.find_one({"showtime_id": showtime_id})
            if showtime:
                print("Dữ liệu suất chiếu từ MongoDB:", showtime)  # In ra để kiểm tra
                self.Movie.setText(showtime.get("movie_id", ""))
                self.Theater.setText(showtime.get("cinema_id", ""))
                self.Room.setText(str(showtime.get("room_id", "")))  # Chuyển room_id thành str
                self.Time.setText(showtime.get("time", ""))
                self.Date.setText(showtime.get("date", ""))
            else:
                QMessageBox.warning(self, "Lỗi", f"Không tìm thấy suất chiếu với ID '{showtime_id}'!")
                self.ID.blockSignals(True)  # Ngăn sự kiện textChanged kích hoạt lại
                self.ID.blockSignals(False)

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi tải dữ liệu suất chiếu:\n{e}")

    def add_showtime(self):
        """Thêm suất chiếu mới vào MongoDB"""
        try:
            showtime_data = self.get_showtime_data()
            if not showtime_data:
                return

            # Kiểm tra ràng buộc
            if not self.validate_showtime_data(showtime_data):
                return

            if self.collection.find_one({"showtime_id": showtime_data["showtime_id"]}):
                QMessageBox.warning(self, "Lỗi", "ID suất chiếu đã tồn tại! Hãy dùng Cập nhật để chỉnh sửa.")
                return

            self.collection.insert_one(showtime_data)
            QMessageBox.information(self, "Thông báo", "Suất chiếu đã được thêm!")
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm suất chiếu:\n{e}")

    def fix_showtime(self):
        """Cập nhật thông tin suất chiếu"""
        try:
            showtime_data = self.get_showtime_data()
            if not showtime_data:
                return

            # Kiểm tra ràng buộc
            if not self.validate_showtime_data(showtime_data):
                return

            result = self.collection.update_one({"showtime_id": showtime_data["showtime_id"]}, {"$set": showtime_data})

            if result.matched_count:
                QMessageBox.information(self, "Thông báo", "Cập nhật suất chiếu thành công!")
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Lỗi", "Suất chiếu không tồn tại! Hãy thêm mới.")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật suất chiếu:\n{e}")

    def delete_showtime(self):
        """Xóa suất chiếu khỏi MongoDB"""
        try:
            showtime_id = self.ID.text().strip()
            if not showtime_id:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID suất chiếu!")
                return

            result = self.collection.delete_one({"showtime_id": showtime_id})

            if result.deleted_count:
                QMessageBox.information(self, "Thông báo", "Xóa suất chiếu thành công!")
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Lỗi", "Suất chiếu không tồn tại!")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa suất chiếu:\n{e}")

    def get_showtime_data(self):
        """Lấy dữ liệu từ form"""
        showtime_id = self.ID.text().strip()
        movie = self.Movie.text().strip()
        theater = self.Theater.text().strip()
        room = self.Room.text().strip()  # Phòng chiếu
        time = self.Time.text().strip()
        date = self.Date.text().strip()

        if not showtime_id or not movie or not theater or not room or not time or not date:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return None

        return {
            "showtime_id": showtime_id,
            "movie_id": movie,
            "cinema_id": theater,
            "room_id": room,  # Phòng chiếu
            "time": time,
            "date": date
        }

    def validate_showtime_data(self, showtime_data):
        """Kiểm tra ràng buộc dữ liệu suất chiếu"""
        # Kiểm tra rạp có trong danh sách và có trạng thái "Hoạt động" không
        theater = self.theaters_collection.find_one({"id": showtime_data["cinema_id"], "status": "Hoạt động"})
        if not theater:
            QMessageBox.warning(self, "Lỗi", f"Rạp '{showtime_data['cinema_id']}' không tồn tại hoặc không hoạt động!")
            return False

        # Kiểm tra phim có trong danh sách và có trạng thái "On-air" không
        movie = self.movies_collection.find_one({"movie_id": showtime_data["movie_id"], "status": "On-air"})
        if not movie:
            QMessageBox.warning(self, "Lỗi", f"Phim '{showtime_data['movie_id']}' không tồn tại hoặc không đang chiếu!")
            return False

        # Kiểm tra phòng chiếu có hợp lệ không
        try:
            # Lấy số phòng từ dữ liệu nhập vào
            room_id = int(showtime_data["room_id"])  # Giả sử room_id là một số nguyên
            max_rooms = theater.get("number_of_rooms", 0)  # Số phòng tối đa của rạp

            if room_id < 1 or room_id > max_rooms:
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    f"Phòng '{room_id}' không tồn tại trong rạp '{showtime_data['cinema_id']}'! "
                    f"Số phòng tối đa của rạp là {max_rooms}."
                )
                return False
        except ValueError:
            QMessageBox.warning(self, "Lỗi", f"Phòng '{showtime_data['room_id']}' không hợp lệ!")
            return False

        return True


    def clear_fields(self):
        """Xóa dữ liệu trên form"""
        self.ID.clear()
        self.Movie.clear()
        self.Theater.clear()
        self.Room.clear()  # Phòng chiếu
        self.Time.clear()
        self.Date.clear()

    def return_to_schedule1(self):
        """Quay về cửa sổ chính"""
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.load_schedule_data()
        self.close()
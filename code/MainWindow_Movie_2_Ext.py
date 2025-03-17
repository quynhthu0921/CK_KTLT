from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class MovieWindow2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("MainWindow_Movie_2.ui", self)  # Load UI
        self.parent_window = parent  # Lưu cửa sổ cha (MovieWindow1)

        # Kết nối MongoDB
        self.collection = self.connect_mongo()

        # Gán sự kiện cho nút
        self.Back.clicked.connect(self.return_to_movie1)
        self.Save.clicked.connect(self.save_movie)
        self.Update.clicked.connect(self.update_movie)

        # Khi nhập ID phim, tự động hiển thị thông tin nếu có
        self.ID.textChanged.connect(self.load_existing_movie)

        # Đảm bảo chỉ chọn 1 trạng thái
        self.Onair.clicked.connect(lambda: self.set_status("On-air"))
        self.Tamngung.clicked.connect(lambda: self.set_status("Tạm ngừng"))
        self.Stop.clicked.connect(lambda: self.set_status("Dừng chiếu"))

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")  # Kết nối
            db = client["data"]
            return db["movie_lst"]
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_existing_movie(self):
        """Tự động hiển thị thông tin nếu phim đã tồn tại dựa theo ID"""
        movie_id = self.ID.text().strip()
        if not movie_id:
            return

        movie = self.collection.find_one({"movie_id": movie_id})
        if movie:
            self.Name.setText(movie.get("name", ""))
            self.Date.setText(movie.get("release_date", ""))
            self.Genre.setText(movie.get("genre", ""))
            self.Des.setPlainText(movie.get("description", ""))

            # Đặt trạng thái
            self.set_status(movie.get("status", ""))
        else:
            # Xóa thông tin cũ nếu nhập ID mới
            self.Name.clear()
            self.Date.clear()
            self.Genre.clear()
            self.Des.clear()
            self.set_status("")  # Bỏ chọn tất cả trạng thái

    def save_movie(self):
        """Thêm phim mới vào MongoDB"""
        movie_data = self.get_movie_data()
        if not movie_data:
            return

        if self.collection.find_one({"movie_id": movie_data["movie_id"]}):
            QMessageBox.warning(self, "Lỗi", "ID phim đã tồn tại! Hãy dùng Update để chỉnh sửa.")
            return

        self.collection.insert_one(movie_data)
        QMessageBox.information(self, "Thông báo", "Phim đã được thêm!")
        self.return_to_movie1()

    def update_movie(self):
        """Cập nhật thông tin phim dựa theo ID"""
        movie_data = self.get_movie_data()
        if not movie_data:
            return

        result = self.collection.update_one({"movie_id": movie_data["movie_id"]}, {"$set": movie_data})

        if result.matched_count:
            QMessageBox.information(self, "Thông báo", "Cập nhật phim thành công!")
            self.return_to_movie1()
        else:
            QMessageBox.warning(self, "Lỗi", "Phim chưa có trong danh sách! Dùng nút Lưu để thêm mới.")

    def get_movie_data(self):
        """Lấy dữ liệu từ form"""
        movie_id = self.ID.text().strip()
        name = self.Name.text().strip()
        release_date = self.Date.text().strip()
        genre = self.Genre.text().strip()
        description = self.Des.toPlainText().strip()

        if not movie_id or not name or not release_date or not genre:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return None

        # Chỉ chọn 1 trạng thái
        status = "On-air" if self.Onair.isChecked() else "Tạm ngừng" if self.Tamngung.isChecked() else "Dừng chiếu"

        return {
            "movie_id": movie_id,  # Thêm ID phim
            "name": name,
            "release_date": release_date,
            "genre": genre,
            "description": description,
            "status": status
        }

    def set_status(self, status):
        """Đảm bảo chỉ một trạng thái được chọn"""
        self.Onair.setChecked(status == "On-air")
        self.Tamngung.setChecked(status == "Tạm ngừng")
        self.Stop.setChecked(status == "Dừng chiếu")

    def return_to_movie1(self):
        """Quay về MovieWindow1 sau khi lưu/cập nhật"""
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.load_movie_data()  # Cập nhật danh sách
        self.close()
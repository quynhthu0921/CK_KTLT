from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class TheaterWindow2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("MainWindow_Theater_2.ui", self)  # Load giao diện từ file .ui
        self.parent_window = parent  # Lưu cửa sổ cha

        # Kết nối MongoDB
        self.collection = self.connect_mongo()

        # Gán sự kiện cho nút
        self.Back.clicked.connect(self.return_to_theater1)
        self.Save.clicked.connect(self.save_theater)
        self.Update.clicked.connect(self.update_theater)

        # Khi nhập ID rạp, tự động hiển thị thông tin nếu có
        self.ID.textChanged.connect(self.load_existing_theater)

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]  # Database name
            return db["theater_lst"]  # Collection name
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_existing_theater(self):
        """Tự động hiển thị thông tin nếu rạp đã tồn tại"""
        theater_id = self.ID.text().strip()
        if not theater_id:
            return

        theater = self.collection.find_one({"id": theater_id})

        if theater:
            self.Name.setText(theater.get("name", ""))
            self.Address.setText(theater.get("address", ""))
            self.Contact.setText(theater.get("contact", ""))
            self.Number.setText(str(theater.get("number_of_rooms", "")))

            # Chỉ cho phép chọn **1 trạng thái** duy nhất
            self.On.setAutoExclusive(False)
            self.Off.setAutoExclusive(False)
            self.Quit.setAutoExclusive(False)

            self.On.setChecked(False)
            self.Off.setChecked(False)
            self.Quit.setChecked(False)

            # Chuyển đổi dữ liệu MongoDB thành trạng thái phù hợp
            status = theater.get("status", "Hoạt động")
            if status == "Hoạt động":
                self.On.setChecked(True)
            elif status == "Tạm dừng":
                self.Off.setChecked(True)
            elif status == "Đóng cửa":
                self.Quit.setChecked(True)

            # Kích hoạt lại autoExclusive
            self.On.setAutoExclusive(True)
            self.Off.setAutoExclusive(True)
            self.Quit.setAutoExclusive(True)


    def save_theater(self):
        """Thêm rạp mới vào MongoDB"""
        try:
            theater_data = self.get_theater_data()
            if not theater_data:
                return

            if self.collection.find_one({"id": theater_data["id"]}):
                QMessageBox.warning(self, "Lỗi", "ID rạp đã tồn tại! Hãy dùng Cập nhật để chỉnh sửa.")
                return

            self.collection.insert_one(theater_data)
            QMessageBox.information(self, "Thông báo", "Rạp chiếu đã được thêm!")
            self.return_to_theater1()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm rạp:\n{e}")

    def update_theater(self):
        """Cập nhật thông tin rạp"""
        try:
            theater_data = self.get_theater_data()
            if not theater_data:
                return

            result = self.collection.update_one({"id": theater_data["id"]}, {"$set": theater_data})

            if result.matched_count:
                QMessageBox.information(self, "Thông báo", "Cập nhật rạp thành công!")
                self.return_to_theater1()
            else:
                QMessageBox.warning(self, "Lỗi", "Rạp không tồn tại! Hãy thêm mới.")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật rạp:\n{e}")

    def get_theater_data(self):
        """Lấy dữ liệu từ form"""
        theater_id = self.ID.text().strip()
        name = self.Name.text().strip()
        address = self.Address.text().strip()
        contact = self.Contact.text().strip()
        number_of_rooms = self.Number.text().strip()

        # Đặt giá trị mặc định trước để tránh lỗi "not defined"
        status = "Hoạt động"  # Giá trị mặc định

        # Chuyển đổi nút sang dữ liệu lưu vào MongoDB
        if self.On.isChecked():
            status = "Hoạt động"
        elif self.Off.isChecked():
            status = "Tạm dừng"
        elif self.Quit.isChecked():
            status = "Đóng cửa"

        if not theater_id or not name or not address or not contact or not number_of_rooms:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return None

        return {
            "id": theater_id,
            "name": name,
            "address": address,
            "contact": contact,
            "number_of_rooms": int(number_of_rooms),
            "status": status  # Lưu đúng trạng thái
        }

    def clear_fields(self):
        """Xóa dữ liệu trên form"""
        self.Name.clear()
        self.Address.clear()
        self.Contact.clear()
        self.Number.clear()

    def return_to_theater1(self):
        """Quay về cửa sổ chính và load lại dữ liệu"""
        if self.parent_window:
            self.parent_window.show()  # Hiển thị TheaterWindow1
            self.parent_window.load_theater_data()  # Cập nhật lại bảng
        self.close()

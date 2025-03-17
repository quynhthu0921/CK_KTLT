from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class StaffWindow2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("MainWindow_Staff_2.ui", self)  # Load giao diện từ file .ui
        self.parent_window = parent  # Lưu cửa sổ cha

        # Kết nối MongoDB
        self.collection = self.connect_mongo()

        # Gán sự kiện cho nút
        self.Back.clicked.connect(self.return_to_staff1)
        self.Save.clicked.connect(self.save_staff)
        self.Update.clicked.connect(self.update_staff)

        # Khi nhập ID nhân viên, tự động hiển thị thông tin nếu có
        self.ID.textChanged.connect(self.load_existing_staff)

        # Chọn trạng thái nhân viên
        self.On.clicked.connect(lambda: self.set_status("Đang làm"))
        self.Off.clicked.connect(lambda: self.set_status("Tạm nghỉ"))
        self.Quit.clicked.connect(lambda: self.set_status("Đã nghỉ"))

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["data"]  # Database name
            return db["staff_lst"]  # Collection name
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_existing_staff(self):
        """Tự động hiển thị thông tin nếu nhân viên đã tồn tại"""
        staff_id = self.ID.text().strip()
        if not staff_id:
            return

        staff = self.collection.find_one({"employee_id": staff_id})

        if staff:
            self.Name.setText(staff.get("name", ""))
            self.Position.setText(staff.get("position", ""))
            self.Salary.setText(str(staff.get("salary", "")))
            self.set_status(staff.get("status"))

            # Không hiển thị cảnh báo, nhưng vẫn cho phép thay đổi trạng thái
            self.enable_status_buttons()
        else:
            self.clear_fields()
            self.enable_status_buttons()

    def save_staff(self):
        """Thêm nhân viên mới vào MongoDB"""
        try:
            staff_data = self.get_staff_data()
            if not staff_data:
                return

            if self.collection.find_one({"employee_id": staff_data["employee_id"]}):
                QMessageBox.warning(self, "Lỗi", "ID nhân viên đã tồn tại! Hãy dùng Cập nhật để chỉnh sửa.")
                return

            self.collection.insert_one(staff_data)
            QMessageBox.information(self, "Thông báo", "Nhân viên đã được thêm!")
            self.return_to_staff1()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm nhân viên:\n{e}")

    def update_staff(self):
        """Cập nhật thông tin nhân viên"""
        try:
            staff_data = self.get_staff_data()
            if not staff_data:
                return

            result = self.collection.update_one({"employee_id": staff_data["employee_id"]}, {"$set": staff_data})

            if result.matched_count:
                QMessageBox.information(self, "Thông báo", "Cập nhật nhân viên thành công!")
                self.return_to_staff1()
            else:
                QMessageBox.warning(self, "Lỗi", "Nhân viên không tồn tại! Hãy thêm mới.")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật nhân viên:\n{e}")

    def get_staff_data(self):
        """Lấy dữ liệu từ form"""
        staff_id = self.ID.text().strip()
        name = self.Name.text().strip()
        position = self.Position.text().strip()
        salary = self.Salary.text().strip()
        status = self.get_status()

        if not staff_id or not name or not position or not salary:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return None

        try:
            salary = int(salary)
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Lương phải là số!")
            return None

        return {
            "employee_id": staff_id,
            "name": name,
            "position": position,
            "salary": salary,
            "status": status
        }

    def set_status(self, status):
        """Thiết lập trạng thái từ database lên UI"""
        self.On.setChecked(status == "Đang làm")
        self.Off.setChecked(status == "Tạm nghỉ")
        self.Quit.setChecked(status == "Đã nghỉ")

    def get_status(self):
        """Lấy trạng thái từ UI"""
        if self.On.isChecked():
            return "Đang làm"
        elif self.Off.isChecked():
            return "Tạm nghỉ"
        elif self.Quit.isChecked():
            return "Đã nghỉ"
        return ""

    def enable_status_buttons(self):
        """Bật lại các nút trạng thái"""
        self.On.setEnabled(True)
        self.Off.setEnabled(True)
        self.Quit.setEnabled(True)

    def clear_fields(self):
        """Xóa dữ liệu trên form"""
        self.Name.clear()
        self.Position.clear()
        self.Salary.clear()
        self.set_status("")

    def return_to_staff1(self):
        """Quay về cửa sổ chính"""
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.load_staff_data()
        self.close()
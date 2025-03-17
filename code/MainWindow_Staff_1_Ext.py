from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from pymongo import MongoClient


class StaffWindow(QMainWindow):
    def __init__(self, home_window=None):  # Nhận home_window
        super().__init__()
        loadUi("MainWindow_Staff_1.ui", self)

        self.home_window = home_window  # Lưu lại tham chiếu HomeWindow

        # Gán sự kiện cho các nút
        self.Update.clicked.connect(self.open_staff_2)
        self.Back.clicked.connect(self.go_back_home)
        self.List.clicked.connect(self.filter_results)

        self.load_staff_data()  # Tải dữ liệu khi mở cửa sổ

    @staticmethod
    def connect_mongo():
        """Kết nối MongoDB"""
        try:
            client = MongoClient("mongodb://localhost:27017/")  # Kết nối MongoDB
            db = client["data"]  # Chọn database
            return db["staff_lst"]  # Trả về collection staff_lst
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi kết nối MongoDB:\n{e}")
            return None

    def load_staff_data(self):
        """Tải dữ liệu từ MongoDB và hiển thị lên bảng (loại bỏ nhân viên đã nghỉ)"""
        collection = self.connect_mongo()
        if collection is None:
            QMessageBox.critical(self, "Lỗi", "Không thể kết nối đến cơ sở dữ liệu!")
            return

        try:
            # Lọc dữ liệu: Chỉ lấy nhân viên có trạng thái khác "Đã nghỉ"
            staff_list = list(collection.find(
                {"status": {"$ne": "Đã nghỉ"}},  # Điều kiện lọc
                {"_id": 0, "employee_id": 1, "name": 1, "position": 1, "salary": 1, "status": 1}
            ))

            # Cấu hình bảng hiển thị
            self.Tab.setRowCount(len(staff_list))
            self.Tab.setColumnCount(5)
            self.Tab.setHorizontalHeaderLabels(["Mã NV", "Tên", "Vị trí", "Lương", "Trạng Thái"])

            # Hiển thị dữ liệu lên bảng
            for row, staff in enumerate(staff_list):
                self.Tab.setItem(row, 0, QTableWidgetItem(staff.get("employee_id", "")))
                self.Tab.setItem(row, 1, QTableWidgetItem(staff.get("name", "")))
                self.Tab.setItem(row, 2, QTableWidgetItem(staff.get("position", "")))
                self.Tab.setItem(row, 3, QTableWidgetItem(str(staff.get("salary", ""))))
                self.Tab.setItem(row, 4, QTableWidgetItem(staff.get("status", "")))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu từ MongoDB:\n{e}")

    def open_staff_2(self):
        """Mở cửa sổ StaffWindow2 để cập nhật thông tin nhân viên"""
        try:
            from MainWindow_Staff_2_Ext import StaffWindow2
            self.staff_window2 = StaffWindow2(self)  # Khởi tạo cửa sổ StaffWindow2
            self.staff_window2.show()  # Hiển thị cửa sổ
            self.hide()  # Ẩn StaffWindow1
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở cửa sổ Staff 2:\n{e}")

    def go_back_home(self):
        """Quay về màn hình chính"""
        self.close()  # Đóng StaffWindow
        if self.home_window:  # Kiểm tra nếu có HomeWindow
            self.home_window.show()  # Hiển thị lại HomeWindow

    def filter_results(self):
        try:

            collection = self.connect_mongo()
            if collection is None:
                QMessageBox.critical(self, "Lỗi", "Không thể kết nối đến MongoDB!")
                return

            # Lấy giá trị được chọn từ các input
            selected_position = self.Position.currentText().strip()
            selected_status = self.Status.currentText().strip()


            # Xây dựng điều kiện tìm kiếm (chỉ thêm nếu có dữ liệu)
            query = {key: value for key, value in {
                "position": selected_position,
                "status": selected_status,

            }.items() if value}  # Chỉ giữ lại các giá trị không rỗng

            # Kiểm tra nếu không có tiêu chí lọc nào được chọn
            if not query:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ít nhất một tiêu chí để lọc!")
                return

            # Truy vấn MongoDB
            results = list(collection.find(
                query, {"_id": 0, "employee_id": 1, "name": 1, "position": 1, "salary": 1, "status": 1}
            ))

            # Kiểm tra nếu không có kết quả
            if not results:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy nhân viên phù hợp!")
                return

            # Hiển thị kết quả lên bảng
            self.Tab.setRowCount(len(results))
            self.Tab.setColumnCount(5)
            self.Tab.setHorizontalHeaderLabels(["Mã NV", "Tên", "Vị trí", "Lương", "Trạng thái"])

            for row, result in enumerate(results):
                self.Tab.setItem(row, 0, QTableWidgetItem(str(result["employee_id"])))
                self.Tab.setItem(row, 1, QTableWidgetItem(result["name"]))
                self.Tab.setItem(row, 2, QTableWidgetItem(result["position"]))
                self.Tab.setItem(row, 3, QTableWidgetItem(str(result["salary"])))
                self.Tab.setItem(row, 4, QTableWidgetItem(result["status"]))

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lọc dữ liệu:\n{e}")

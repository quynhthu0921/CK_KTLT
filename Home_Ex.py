from PyQt6 import QtWidgets
from pymongo import MongoClient
from Home import Ui_Home
from Cinema_Ex import Cinema  # Import giao diện chọn rạp phim


class Home(Ui_Home):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Kết nối MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["_database"]  # Thay đổi tên database theo yêu cầu
        self.collection = self.db["booking"]  # Tạo collection để lưu phim đã chọn

        # Lưu danh sách các nút "Mua ngay" và tên phim tương ứng
        self.movies = {
            self.buy1: "Flow - Lạc Trôi",
            self.buy2: "Nhà Gia Tiên",
            self.buy3: "Interstella",
            self.buy4: "Quỷ Nhập Tràng",
            self.buy5: "Cưới Ma",
            self.buy6: "Nữ Tu Bóng Tối",
            self.buy7: "Attack On Titan",
            self.buy8: "Nụ Hôn Bạc Tỷ",
        }

        # Gán sự kiện bấm nút cho từng button "Mua ngay"
        for button in self.movies.keys():
            button.clicked.connect(self.save_movie_selection)

    def save_movie_selection(self):
        sender_button = self.MainWindow.sender()  # Lấy button được bấm
        selected_movie = self.movies.get(sender_button, "")

        if selected_movie:
            # Tạo một booking mới với chỉ tên phim
            booking_data = {
                "Tên phim": selected_movie,
                "Rạp chiếu": None,
                "Ngày chiếu": None,
                "Suất chiếu": None,
                "Chỗ ngồi": None,
                "Combo": None
            }
            booking_id = self.collection.insert_one(booking_data).inserted_id  # Lưu ID để cập nhật sau

            # Lưu ID này vào file tạm để sử dụng trong các bước tiếp theo
            with open("current_booking_id.txt", "w") as file:
                file.write(str(booking_id))

            # Chuyển sang giao diện chọn rạp phim
            self.cinema_window = QtWidgets.QMainWindow()
            self.cinema_ui = Cinema()
            self.cinema_ui.setupUi(self.cinema_window)

            self.MainWindow.hide()
            self.cinema_window.show()

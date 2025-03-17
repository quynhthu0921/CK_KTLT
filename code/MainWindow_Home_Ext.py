from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from MainWindow_Staff_1_Ext import StaffWindow
from MainWindow_Movie_1_Ext import MovieWindow
from MainWindow_Theater_1_Ext import TheaterWindow
from MainWindow_Schedule_1_Ext import ScheduleWindow
from MainWindow_Statics_Ext import StaticsWindow


class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("MainWindow_Home.ui", self)

        self.current_window = None  # Lưu trạng thái cửa sổ hiện tại

        # Gán sự kiện cho các nút
        self.Staff.clicked.connect(self.open_staff_window)
        self.Movie.clicked.connect(self.open_movie_window)
        self.Theater.clicked.connect(self.open_theater_window)
        self.Schedule.clicked.connect(self.open_schedule_window)
        self.Statics.clicked.connect(self.open_statics_window)


    def open_window(self, window_class):
        """Đóng cửa sổ hiện tại trước khi mở cửa sổ mới"""
        try:
            if self.current_window:
                self.current_window.close()

            self.current_window = window_class(self)  # Truyền Home vào cửa sổ con
            self.current_window.show()
            self.hide()  # Ẩn Home
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở cửa sổ:\n{e}")

    def open_staff_window(self):
        """Mở cửa sổ quản lý nhân viên"""
        self.open_window(StaffWindow)

    def open_movie_window(self):
        """Mở cửa sổ quản lý phim"""
        self.open_window(MovieWindow)

    def open_theater_window(self):
        """Mở cửa sổ quản lý rạp"""
        self.open_window(TheaterWindow)

    def open_schedule_window(self):
        """Mở cửa sổ quản lý lịch chiếu"""
        self.open_window(ScheduleWindow)

    def open_statics_window(self):
        """Mở cửa sổ quản lý lịch chiếu"""
        self.open_window(StaticsWindow)


    def return_to_home(self):
        """Quay về màn hình chính"""
        if self.current_window:
            self.current_window.close()
        self.current_window = None
        self.show()

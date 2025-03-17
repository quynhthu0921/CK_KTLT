import random
from datetime import datetime, timedelta
import json  # Thêm thư viện json

# Danh sách rạp và số phòng tương ứng
theaters = {
    "R001": 5,
    "R002": 7,
    "R003": 7,
    "R004": 6,
    "R005": 5,
    "R006": 4,
    "R007": 4
}

# Danh sách phim
movies = [f"MV{i:03d}" for i in range(1, 9)]  # MV001 đến MV008

# Ngày chiếu (7 ngày đầu tháng 4 năm 2025)
start_date = datetime(2025, 4, 1)
dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

# Giờ chiếu (từ 10:00 đến 22:00)
times = [f"{hour:02d}:{minute:02d}" for hour in range(10, 23) for minute in [0, 30]]

# Hàm tạo dữ liệu
def generate_showtimes(num_showtimes=500):
    showtimes = []
    for i in range(1, num_showtimes + 1):
        # Tạo showtime_id
        showtime_id = f"ST{i:03d}"

        # Chọn ngẫu nhiên rạp và phòng chiếu
        cinema_id = random.choice(list(theaters.keys()))
        max_rooms = theaters[cinema_id]
        room_id = random.randint(1, max_rooms)

        # Chọn ngẫu nhiên phim, ngày và giờ
        movie_id = random.choice(movies)
        date = random.choice(dates)
        time = random.choice(times)

        # Tạo dữ liệu suất chiếu
        showtime = {
            "showtime_id": showtime_id,
            "cinema_id": cinema_id,
            "movie_id": movie_id,
            "room_id": room_id,
            "date": date,
            "time": time
        }
        showtimes.append(showtime)

    return showtimes

# Tạo 500 dòng dữ liệu
data = generate_showtimes(500)

# In ra dưới dạng JSON
print(json.dumps(data, indent=4))
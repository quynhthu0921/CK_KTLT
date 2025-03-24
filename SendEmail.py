import smtplib
import random
from email.mime.text import MIMEText

def send_email(email):
    sender_email = "thuphuongdangha@gmail.com"
    sender_password = "grqu vcqo nlhe qljb"

    msg = MIMEText(f"Cảm ơn bạn đã đăng ký tài khoản CineSnack!")
    msg["Subject"] = "CineSnack - Mã xác thực"
    msg["From"] = "[No reply] - OTP"
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Lỗi gửi email:", e)
        return None

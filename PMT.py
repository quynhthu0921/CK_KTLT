from PyQt6.QtWidgets import QApplication, QMainWindow
from CompletedPurchaseScreen_EXT import UI_Ext_ForgetPassword
import sys

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

w = QMainWindow()
f = UI_Ext_ForgetPassword()
f.setupUi(w)

w.show()

sys.exit(app.exec())
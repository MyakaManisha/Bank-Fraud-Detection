import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from Mainprofile import Ui_MainWindow
from registrationNew import Ui_registrationPage

class Ui_LoginWindow(QMainWindow):  # Inherit from QMainWindow to override resizeEvent
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, LoginWindow):
        self.loginWindow = LoginWindow
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.setWindowTitle(" 🛡️BANK FRAUD DETECTION")
        LoginWindow.setGeometry(100, 100, 1200, 700)
        LoginWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint
        )

        self.failed_attempts = {}

        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        LoginWindow.setCentralWidget(self.centralwidget)

        # Background image using QLabel
        self.bg_label = QtWidgets.QLabel(self.centralwidget)
        self.bg_label.setGeometry(0, 0, 1200, 700)
        self.bg_label.setScaledContents(True)
        self.bg_label.setPixmap(QtGui.QPixmap(r"D:\python stuff\bank.jpg").scaled(
            LoginWindow.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation
        ))

        # Transparent login panel
        self.panel = QtWidgets.QFrame(self.centralwidget)
        self.panel.setGeometry(QtCore.QRect(400, 150, 400, 400))
        self.panel.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 15px;
            }
        """)

        # Fade-in animation
        opacity_effect = QGraphicsOpacityEffect(self.panel)
        self.panel.setGraphicsEffect(opacity_effect)
        self.fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        self.fade_in.setDuration(1000)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_in.start()

        # Logo
        self.logo = QtWidgets.QLabel(self.panel)
        self.logo.setGeometry(QtCore.QRect(0, 30, 400, 50))
        self.logo.setText("🏦 Bank Login")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setStyleSheet("font: bold 24pt 'Segoe UI'; color: #2c3e50;")

        # Username
        self.lineEdit_username = QtWidgets.QLineEdit(self.panel)
        self.lineEdit_username.setGeometry(QtCore.QRect(80, 100, 240, 40))
        self.lineEdit_username.setFont(QtGui.QFont("Segoe UI", 11))
        self.lineEdit_username.setPlaceholderText("Enter Username")
        self.lineEdit_username.setStyleSheet("""
            QLineEdit {
                background-color: #f5f6fa;
                border: 2px solid #dcdde1;
                border-radius: 10px;
                padding-left: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

        # Password
        self.lineEdit_password = QtWidgets.QLineEdit(self.panel)
        self.lineEdit_password.setGeometry(QtCore.QRect(80, 160, 240, 40))
        self.lineEdit_password.setFont(QtGui.QFont("Segoe UI", 11))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText("Enter Password")
        self.lineEdit_password.setStyleSheet("""
            QLineEdit {
                background-color: #f5f6fa;
                border: 2px solid #dcdde1;
                border-radius: 10px;
                padding-left: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

        # Login button
        self.pushButton_login = QtWidgets.QPushButton(self.panel)
        self.pushButton_login.setGeometry(QtCore.QRect(150, 230, 100, 35))
        self.pushButton_login.setText("Login")
        self.pushButton_login.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
                transform: scale(1.1);
            }
        """)
        self.pushButton_login.clicked.connect(self.loginClicked)

        # Register button
        self.pushButton_register = QtWidgets.QPushButton(self.panel)
        self.pushButton_register.setGeometry(QtCore.QRect(150, 280, 100, 35))
        self.pushButton_register.setText("Register")
        self.pushButton_register.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #3498db;
                transform: scale(1.1);
            }
        """)
        self.pushButton_register.clicked.connect(self.openRegisterPage)

    def resizeEvent(self, event):
        # Make background image responsive
        self.bg_label.setPixmap(QtGui.QPixmap(r"D:\python stuff\bank.jpg").scaled(
            self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation
        ))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

    def message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.exec_()

    def loginClicked(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()

        if not username or not password:
            self.message('Input Error', 'Please enter both username and password.')
            return

        conn = sqlite3.connect("BankNH.db")
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM NEWBANK WHERE USERNAME = ?", (username,))
        result = cur.fetchone()
        conn.close()

        try:
            if result and result[0] == int(password):
                self.failed_attempts[username] = 0
                self.gotoProfile(username)
            else:
                self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
                if self.failed_attempts[username] >= 5:
                    self.message("⚠ Fraud Alert", f"Multiple failed attempts detected for user '{username}'.")
                    self.shakeEffect()
                else:
                    self.message("Login Failed", "Incorrect username or password.")
        except ValueError:
            self.message("Error", "Password must be a number.")

    def gotoProfile(self, username):
        self.loginWindow.close()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def openRegisterPage(self):
        self.registerWindow = QtWidgets.QMainWindow()
        self.ui = Ui_registrationPage()
        self.ui.setupUi(self.registerWindow)
        self.registerWindow.show()

    def shakeEffect(self):
        shake_animation = QPropertyAnimation(self.panel, b"geometry")
        shake_animation.setDuration(300)
        shake_animation.setKeyValueAt(0, QRect(400, 150, 400, 400))
        shake_animation.setKeyValueAt(0.1, QRect(390, 150, 400, 400))
        shake_animation.setKeyValueAt(0.2, QRect(410, 150, 400, 400))
        shake_animation.setKeyValueAt(0.3, QRect(390, 150, 400, 400))
        shake_animation.setKeyValueAt(0.4, QRect(410, 150, 400, 400))
        shake_animation.setKeyValueAt(0.5, QRect(400, 150, 400, 400))
        shake_animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_LoginWindow()
    window.show()
    sys.exit(app.exec_())

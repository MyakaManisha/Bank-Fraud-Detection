from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QInputDialog, QLineEdit
import sqlite3

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)  # Increased size

        # Set window title
        MainWindow.setWindowTitle("BANK FRAUD DETECTION")

        # Set background image
        background = QtGui.QPixmap(r"D:\python stuff\bank.jpg")  # <-- Replace with your image
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(background.scaled(MainWindow.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        MainWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Title with pure white color
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font: bold 22pt 'Verdana'; color: white; background: transparent;")  # Pure white color
        self.label.setText("🏦 BANK DETAILS")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        # Image
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("bank_icon.png")
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(140, 140, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        
        # Buttons layout
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        # Button Style (Bold Text in Dark Black Color)
        button_style = (
            "background-color: rgba(255, 255, 255, 0.85);"
            "font: bold 12pt 'Verdana';"
            "color: rgb(0, 0, 0);"  # Dark black color
            "padding: 10px;"
            "border-radius: 10px;"
            "transition: all 0.3s ease;"
        )

        # Define Buttons
        self.pushButton_balance = QtWidgets.QPushButton("BALANCE", self.centralwidget)
        self.pushButton_balance.setStyleSheet(button_style)
        self.gridLayout.addWidget(self.pushButton_balance, 0, 0)

        self.pushButton_transfer = QtWidgets.QPushButton("TRANSFER", self.centralwidget)
        self.pushButton_transfer.setStyleSheet(button_style)
        self.gridLayout.addWidget(self.pushButton_transfer, 1, 0)

        self.pushButton_deposit = QtWidgets.QPushButton("DEPOSIT MONEY", self.centralwidget)
        self.pushButton_deposit.setStyleSheet(button_style)
        self.gridLayout.addWidget(self.pushButton_deposit, 2, 0)

        self.pushButton_deleteAccount = QtWidgets.QPushButton("DELETE ACCOUNT", self.centralwidget)
        self.pushButton_deleteAccount.setStyleSheet(button_style)
        self.gridLayout.addWidget(self.pushButton_deleteAccount, 3, 0)

        self.pushButton_logout = QtWidgets.QPushButton("LOG OUT", self.centralwidget)
        self.pushButton_logout.setStyleSheet(button_style)
        self.gridLayout.addWidget(self.pushButton_logout, 4, 0)

        self.gridLayout_2.addLayout(self.gridLayout, 2, 0)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu + Statusbar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Button connections
        self.pushButton_balance.clicked.connect(self.CheckBal)
        self.pushButton_transfer.clicked.connect(self.Transfer)
        self.pushButton_deleteAccount.clicked.connect(self.DeleteAcc)
        self.pushButton_logout.clicked.connect(self.Logout)
        self.pushButton_deposit.clicked.connect(self.DepositMoney)

    def CheckBal(self):
        import sqlite3

        # Get the password from the user
        password, okPressed = QInputDialog.getText(self, "Check Balance", "Please Enter Your Password:",
                                                   QtWidgets.QLineEdit.Password)

        # Check if the user pressed OK and entered a password
        if okPressed and password:
            conn = sqlite3.connect('BankNH.db')
            cur = conn.cursor()

            # Check if the entered password matches a record in the database
            cur.execute("SELECT BAL FROM NEWBANK WHERE PASSWORD = ?", (password,))
            data = cur.fetchone()

            if data is not None:
                # Display the balance
                balance = data[0]
                QMessageBox.information(self, "Balance", f"Your balance is: {balance}")
            else:
                # Show an error message for incorrect password
                QMessageBox.warning(self, "Invalid Password", "Invalid password. Please try again.")
        else:
            # Show an error message if no password was entered
            QMessageBox.warning(self, "Invalid Input", "Invalid input. Please enter a password.")

    def Transfer(self):
        self.mainwindow.close()
        from Transfer import Ui_TransferWindow # type: ignore
        self.TransferWindow = self.mainwindow
        self.ui = Ui_TransferWindow()
        self.ui.setupUi(self.TransferWindow)
        self.TransferWindow.show()

    def DepositMoney(self):
        username, okPressed = QInputDialog.getText(self, "Deposit Money", "Enter the Username:")
        if okPressed and username:
            amount, okPressed = QInputDialog.getDouble(self, "Deposit Money", "Enter Amount to Deposit:")
            if okPressed and amount > 0:
                print(f"Attempting to deposit {amount} to {username}...")  # Debug print
                # Connect to the database and deposit the amount
                conn = sqlite3.connect('BankNH.db')
                cur = conn.cursor()

                # Update the balance of the user in the database
                cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME = ?", (username,))
                cur_balance = cur.fetchone()
                if(cur_balance == None):
                    cur.execute("UPDATE NEWBANK SET BAL =  ? WHERE USERNAME = ?", (amount, username))
                    conn.commit()
                else:
                    cur.execute("UPDATE NEWBANK SET BAL = BAL + ? WHERE USERNAME = ?", (amount, username))
                    conn.commit()

                # Fetch the updated balance and show it
                cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME = ?", (username,))
                updated_balance = cur.fetchone()

                conn.close()

                if updated_balance:
                    print(f"Deposit successful. Updated balance: {updated_balance[0]}")  # Debug print
                    # Inform the user and show the updated balance
                    QMessageBox.information(self, "Deposit Successful",
                                            f"Amount of {amount} deposited to {username}'s account.\n"
                                            f"Updated balance: {updated_balance[0]}")
                else:
                    print("User not found or update failed.")  # Debug print
                    QMessageBox.warning(self, "User Not Found", "The username provided does not exist.")
            else:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid amount to deposit.")
        else:
            QMessageBox.warning(self, "Invalid Username", "Please enter a valid username.")

    def DeleteAcc(self):
        import sqlite3
        from PyQt5.QtWidgets import QMessageBox

        conn = sqlite3.connect("BankNH.db")
        cur = conn.cursor()

        password, okPressed = QInputDialog.getText(self, "Delete Account", "Please Enter Your Password:",
                                                   QtWidgets.QLineEdit.Password)

        if okPressed:
            # Check if the password matches a record in the database
            cur.execute("SELECT * FROM NEWBANK WHERE PASSWORD = ?", (password,))
            user_data = cur.fetchone()

            if user_data is not None:
                # If a matching user is found, delete the user's record
                cur.execute("DELETE FROM NEWBANK WHERE PASSWORD = ?", (password,))
                conn.commit()
                conn.close()

                # Show a success message
                QMessageBox.information(self, "Account Deleted", "Your account has been successfully deleted.")
            else:
                conn.close()
                # Show an error message for incorrect password
                QMessageBox.warning(self, "Deletion Failed", "Incorrect password. Account not deleted.")
        else:
            self.mainwindow.show()

    def Logout(self):
        # Ask the user for confirmation
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            # User confirmed, close the application
            quit()
        else:
            # User canceled, return to the dashboard or take appropriate action
            self.setupUi(MainWindow)  # Replace with the actual function to show the dashboard

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_balance.setText(_translate("MainWindow", "BALANCE"))
        self.pushButton_deleteAccount.setText(_translate("MainWindow", "DELETE ACCOUNT"))
        self.pushButton_transfer.setText(_translate("MainWindow", "TRANSFER"))
        self.pushButton_logout.setText(_translate("MainWindow", "LOG OUT"))
        self.pushButton_deposit.setText(_translate("MainWindow", "DEPOSIT MONEY"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import sys
import random
import sqlite3
import joblib
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from Mainprofile import Ui_MainWindow

class Ui_TransferWindow(object):
    def setupUi(self, TransferWindow):
        self.transfer = TransferWindow
        TransferWindow.setObjectName("TransferWindow")
        TransferWindow.resize(1000, 700)
        TransferWindow.setStyleSheet("background-color: white;")

        self.centralwidget = QtWidgets.QWidget(TransferWindow)

        # Background image
        self.bg_label = QtWidgets.QLabel(self.centralwidget)
        self.bg_label.setGeometry(0, 0, 1000, 700)
        self.bg_label.setPixmap(QtGui.QPixmap(r"D:\python stuff\bank.jpg").scaled(
            1000, 700, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation
        ))
        self.bg_label.lower()  # Send background behind all widgets

        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(100, 80, 800, 250))
        self.gridLayout = QtWidgets.QGridLayout(self.formLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        label_style = "font: 75 12pt 'Verdana'; color: black;"
        input_style = "background-color: white; font: 75 10pt 'Verdana'; color: black;"

        # Labels and input fields with proper spacing
        self.label_amount2txf = QtWidgets.QLabel("ENTER AMOUNT TO DEPOSIT")
        self.label_amount2txf.setStyleSheet(label_style)
        self.gridLayout.addWidget(self.label_amount2txf, 0, 0)
        
        self.lineEdit_amount2txf = QtWidgets.QLineEdit()
        self.lineEdit_amount2txf.setStyleSheet(input_style)
        self.gridLayout.addWidget(self.lineEdit_amount2txf, 0, 1)

        self.label_name2txf = QtWidgets.QLabel("Sender username")
        self.label_name2txf.setStyleSheet(label_style)
        self.gridLayout.addWidget(self.label_name2txf, 1, 0)

        self.lineEdit_name2txf = QtWidgets.QLineEdit()
        self.lineEdit_name2txf.setStyleSheet(input_style)
        self.gridLayout.addWidget(self.lineEdit_name2txf, 1, 1)

        self.label_number2txf = QtWidgets.QLabel("Receiver username")
        self.label_number2txf.setStyleSheet(label_style)
        self.gridLayout.addWidget(self.label_number2txf, 2, 0)

        self.lineEdit_number2txf = QtWidgets.QLineEdit()
        self.lineEdit_number2txf.setStyleSheet(input_style)
        self.gridLayout.addWidget(self.lineEdit_number2txf, 2, 1)

        self.comboBox_accountType = QtWidgets.QComboBox()
        self.comboBox_accountType.setStyleSheet("font: 75 10pt 'Verdana'; color: black;")
        self.comboBox_accountType.addItems(["Type", "CASH_OUT", "TRANSFER"])
        self.gridLayout.addWidget(self.comboBox_accountType, 3, 0, 1, 2)

        self.comboBox_bankType = QtWidgets.QComboBox()
        self.comboBox_bankType.setStyleSheet("font: 75 10pt 'Verdana'; color: black;")
        self.comboBox_bankType.addItems([ 
            "Choose Bank Name Below", "FirstBank", "GTB", "STABIC", "POLARIS", "FCMB", "ACCESS", "Others"
        ])
        self.gridLayout.addWidget(self.comboBox_bankType, 4, 0, 1, 2)

        # Add some space between rows for clarity
        self.gridLayout.setVerticalSpacing(20)

        # Adjust the position of the transfer and cancel buttons
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(350, 400, 300, 120))
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget_2)

        # Modern glassy buttons
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                font: bold 12pt 'Verdana';
                color: black;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 255, 230);
            }
        """

        self.pushButton_transferTransfer = QtWidgets.QPushButton("TRANSFER")
        self.pushButton_transferTransfer.setStyleSheet(button_style)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pushButton_transferTransfer)

        self.pushButton_transferCancle = QtWidgets.QPushButton("CANCEL")
        self.pushButton_transferCancle.setStyleSheet(button_style.replace("black", "red"))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton_transferCancle)

        # Adding space between the buttons
        self.formLayout.setVerticalSpacing(30)  # Increases space between the buttons

        TransferWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TransferWindow)
        TransferWindow.setMenuBar(self.menubar)

        self.pushButton_transferTransfer.clicked.connect(self.SendTransfer)
        self.pushButton_transferCancle.clicked.connect(self.CancleTxf)

    def message(self, title, message):
        mssg = QMessageBox()
        mssg.setWindowTitle(title)
        mssg.setIcon(QMessageBox.Warning)
        mssg.setStandardButtons(QMessageBox.Ok)
        mssg.setText(message)
        mssg.exec_()

    def SendTransfer(self):
        conn = sqlite3.connect("BankNH.db")
        cur = conn.cursor()

        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS NEWT (
                SENDER TEXT,
                RECEIVER TEXT,
                TTYPE TEXT,
                AMOUNT REAL,
                SENDEROLDBAL REAL,
                SENDERNEWBAL REAL,
                RECOLDBAL REAL,
                RECNEWBAL REAL
            );
        """)

        sender_username = self.lineEdit_name2txf.text().strip()
        amount_str = self.lineEdit_amount2txf.text().strip()
        receiver_username = self.lineEdit_number2txf.text().strip()
        selected_type = self.comboBox_accountType.currentText()

        try:
            if not sender_username or not receiver_username or not amount_str:
                self.message('Input Error', 'Please fill in all required fields.')
                return

            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero")

            cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME = ?", (sender_username,))
            sender_result = cur.fetchone()
            if sender_result is None or sender_result[0] is None:
                self.message('Sender Error', 'Sender not found or has no balance.')
                return
            sender_balance = float(sender_result[0])

            if sender_balance < amount:
                self.message('Insufficient Funds', 'Sender does not have enough balance.')
                self.message('Declined Funds Transfer', 'FRAUDULENT ACTION DETECTED')
                return

            cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME = ?", (receiver_username,))
            receiver_result = cur.fetchone()
            if receiver_result is None or receiver_result[0] is None:
                self.message('Receiver Error', 'Receiver not found or has no balance.')
                return
            receiver_balance = float(receiver_result[0])

            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount

            cur.execute("UPDATE NEWBANK SET BAL = ? WHERE USERNAME = ?", (new_sender_balance, sender_username))
            cur.execute("UPDATE NEWBANK SET BAL = ? WHERE USERNAME = ?", (new_receiver_balance, receiver_username))
            self.message('Transfer Detail', '✅Successful Transfer of amount')
            cur.execute(""" 
                INSERT INTO NEWT (SENDER, RECEIVER, TTYPE, AMOUNT, SENDEROLDBAL, SENDERNEWBAL, RECOLDBAL, RECNEWBAL)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sender_username,
                receiver_username,
                selected_type,
                amount,
                sender_balance,
                new_sender_balance,
                receiver_balance,
                new_receiver_balance
            ))

            conn.commit()

            features = [
                random.randint(0, 9),
                selected_type,
                amount,
                sender_balance,
                new_sender_balance,
                receiver_balance,
                new_receiver_balance
            ]

            self.load(features)

        except ValueError:
            self.message('Invalid Amount', 'Enter a valid numeric amount.')
        except sqlite3.Error as e:
            self.message('Database Error', str(e))
        finally:
            conn.close()

    def CancleTxf(self):
        self.transfer.close()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def pipeline(self, df):
        num_feats = df.drop(["type"], axis=1)
        num_feats_pipe = Pipeline([("scaler", MinMaxScaler())])
        cat_feats = df[["type"]]
        cat_feats_pipe = Pipeline([("encoder", OneHotEncoder())])
        final_pipeline = ColumnTransformer([
            ("num", num_feats_pipe, list(num_feats)),
            ("cat", cat_feats_pipe, ["type"])
        ])
        return final_pipeline.fit_transform(df)

    def load(self, list_data):
        df = pd.DataFrame([list_data], columns=[
            'count', 'type', 'amount', 'oldbalanceOrig', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'
        ])
        model = joblib.load("fraud_detection_model.pkl")
        prediction = model.predict(df)
        result_msg = '✅ Transaction Successful!' if prediction[0] == 0 else '⚠ Fraudulent Transaction Detected!'

        QMessageBox.information(None, "Transaction Result", result_msg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TransferWindow = QtWidgets.QMainWindow()
    ui = Ui_TransferWindow()
    ui.setupUi(TransferWindow)
    TransferWindow.show()
    sys.exit(app.exec_())

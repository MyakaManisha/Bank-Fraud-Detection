from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QMessageBox

dbb = sqlite3.connect('BankNH.db')
c = dbb.cursor()

class Ui_registrationPage(object):
    def setupUi(self, registrationPage):
        self.register = registrationPage
        registrationPage.setObjectName("registrationPage")
        registrationPage.resize(800, 600)  # Increased window size for better spacing
        registrationPage.setStyleSheet("background-color: rgb(111, 87, 130);")
        self.centralwidget = QtWidgets.QWidget(registrationPage)
        self.centralwidget.setObjectName("centralwidget")
        
        # Centering the form layout and adjusting margins/paddings
        self.formLayout_2 = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout_2.setAlignment(QtCore.Qt.AlignCenter)  # Center the form in the window

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setObjectName("formLayout")
        
        # Labels and Fields with modernized styling
        self.label_username = self.createLabel("Username")
        self.lineEdit_Username = self.createLineEdit("Username")

        self.label_fname = self.createLabel("First Name")
        self.lineEdit_Firstname = self.createLineEdit("First name")

        self.label_Lname = self.createLabel("Last Name")
        self.lineEdit_Lastname = self.createLineEdit("Last name")

        self.label_email = self.createLabel("Email")
        self.lineEdit_email = self.createLineEdit("Email")

        self.label_password = self.createLabel("Password")
        self.lineEdit_password = self.createLineEdit("Password", echo=True)

        self.label_password_confirm = self.createLabel("Confirm Password")
        self.lineEdit_confirmPassword = self.createLineEdit("Confirm Password", echo=True)

        self.label_phone = self.createLabel("Phone")
        self.lineEdit_phone = self.createLineEdit("Phone number")

        self.label_sex = self.createLabel("Sex")
        self.comboBox_sex = self.createComboBox(["Male", "Female", "Other"])

        self.label_address = self.createLabel("Address")
        self.lineEdit_address = self.createLineEdit("Address")

        self.pushButton_Register = self.createButton("REGISTER")
        self.pushButton_reglogin = self.createButton("LOGIN")

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_username)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Username)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_fname)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Firstname)

        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Lname)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Lastname)

        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_email)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_email)

        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)

        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_password_confirm)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_confirmPassword)

        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_phone)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_phone)

        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_sex)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.comboBox_sex)

        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_address)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.lineEdit_address)

        self.formLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.pushButton_Register)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.pushButton_reglogin)

        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.formLayout)

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setStyleSheet("color: rgb(252, 252, 252); font: 75 20pt 'MS Shell Dlg 2';")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setText("REGISTRATION PAGE")

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_10)

        registrationPage.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(registrationPage)
        registrationPage.setStatusBar(self.statusbar)

        self.retranslateUi(registrationPage)
        QtCore.QMetaObject.connectSlotsByName(registrationPage)

        self.pushButton_Register.clicked.connect(self.CreateDB)
        self.pushButton_reglogin.clicked.connect(self.login)

    def createLabel(self, text):
        label = QtWidgets.QLabel(self.centralwidget)
        label.setStyleSheet("color: rgb(252, 252, 252); font: 75 12pt 'Verdana';")
        label.setText(text)
        return label

    def createLineEdit(self, placeholder, echo=False):
        lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        lineEdit.setStyleSheet("font: 75 10pt 'Verdana'; background-color: rgb(240, 240, 240); padding: 5px;")
        lineEdit.setPlaceholderText(placeholder)
        if echo:
            lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        return lineEdit

    def createComboBox(self, items):
        comboBox = QtWidgets.QComboBox(self.centralwidget)
        comboBox.addItems(items)
        comboBox.setStyleSheet("font: 75 10pt 'Verdana'; background-color: rgb(240, 240, 240); padding: 5px;")
        return comboBox

    def createButton(self, text):
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setStyleSheet("font: 75 10pt 'MS Shell Dlg 2'; color: rgb(240, 240, 240); "
                             "background-color: rgb(78, 78, 78); border-radius: 8px; padding: 10px;")
        button.setText(text)
        return button

    def general_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Question)
        msg.exec_()

    def CreateDB(self):
        c.execute(''' CREATE TABLE IF NOT EXISTS NEWBANK(
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           USERNAME CHAR(20) NOT NULL,
           FIRSTNAME STR NOT NULL,
           LASTNAME STR NOT NULL,
           EMAIL STR NOT NULL,
           PASSWORD STR NOT NULL,
           CONFIRM STR NOT NULL,
           PHONE CHAR(11) NOT NULL,
           SEX STR,
           ADDRESS CHAR(50) NOT NULL,
           BAL REAL(200) );
           ''')
        self.insertdb()
    def openlogin(self):
        from MainLogin import Ui_LoginWindow
        self.register.close()  
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self.LoginWindow)
        self.LoginWindow.show()


    def insertdb(self):
        username = self.lineEdit_Username.text()
        firstname = self.lineEdit_Firstname.text()
        lastname = self.lineEdit_Lastname.text()
        email = self.lineEdit_email.text()
        if '@' not in email:
            self.general_message('Invalid Email', 'Please Check your Email again')
            return email
        else:
            password = self.lineEdit_password.text()
            confirmPass = self.lineEdit_confirmPassword.text()
            if password != confirmPass:
                self.general_message('password Error', 'Password Not Match')
                return password and confirmPass
            elif len(password) != len(confirmPass):
                self.general_message('password Error', 'password not Match')
                return password and confirmPass
            else:
                phone = self.lineEdit_phone.text()
                if len(phone) != 11:
                    self.general_message('Invalid Number', 'please Check your Phone number')
                    return phone
                else:
                    sex = self.comboBox_sex.currentText()
                    address = self.lineEdit_address.text()
                    c.execute("INSERT INTO NEWBANK(USERNAME, FIRSTNAME, LASTNAME, EMAIL, PASSWORD, CONFIRM, PHONE, SEX ,ADDRESS,BAL)VALUES (?,?,?,?,?,?,?,?,?,?)", (str(username), str(firstname), str(lastname), str(email), str(password), str(confirmPass), str(phone), str(sex), str(address),0.0))
                    self.general_message('Registration Result', 'New User Added Successfully')
                    self.openlogin()
                    # self.r                    
                    dbb.commit()
                    dbb.close()
       

    def login(self):
        from registrationNew import Ui_registrationPage  # ✅ Safe lazy import
        self.register.close()
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui.beginLogin(self.LoginWindow)
        self.LoginWindow.show()

    def retranslateUi(self, registrationPage):
        _translate = QtCore.QCoreApplication.translate
        registrationPage.setWindowTitle(_translate("registrationPage", "Registration Page"))
        self.pushButton_Register.setText(_translate("registrationPage", "REGISTER"))
        self.pushButton_reglogin.setText(_translate("registrationPage", "LOGIN"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    registrationPage = QtWidgets.QMainWindow()
    ui = Ui_registrationPage()
    ui.setupUi(registrationPage)
    registrationPage.show()
    sys.exit(app.exec_())
from PyQt6 import QtCore, QtGui, QtWidgets
from github_api import get_user_info
import requests


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 30, 231, 32))
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setClearButtonEnabled(True)
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 100, 111, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Github User Info"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter a username"))
        self.lineEdit.setStatusTip(_translate("MainWindow", "Enter a username"))
        self.pushButton.setText(_translate("MainWindow", "Get User Info"))

        self.lineEdit.returnPressed.connect(self.get_user_info)
        self.pushButton.clicked.connect(self.get_user_info)

    def get_user_info(self):
        username = self.lineEdit.text()
        self.statusbar.showMessage(f"Getting user info for {username}...")
        user_info = get_user_info(username)
        if user_info:
            self.statusbar.hide()
            self.show_user_info(user_info)
        else:
            self.statusbar.showMessage("User not found.")
            self.statusbar.show()

    def dl_profile_pic(self, user_info):
        profile_pic_url = user_info["avatar_url"]
        profile_pic = requests.get(profile_pic_url)
        with open("profile_pic.jpg", "wb") as file:
            file.write(profile_pic.content)
            file.close()

    def show_user_info(self, user_info):
        self.user_info_window = QtWidgets.QMainWindow()
        self.user_info_window.setObjectName("User Info")
        self.user_info_window.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(parent=self.user_info_window)
        self.centralwidget.setObjectName("centralwidget")
        self.user_info_window.setWindowTitle(user_info["login"])
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 10, 111, 101))
        self.dl_profile_pic(user_info)
        self.label.setPixmap(QtGui.QPixmap("profile_pic.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("profile_pic")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(80, 130, 241, 141))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlainText(
            f"Name: {user_info['name']}\n"
            f"Location: {user_info['location']}\n"
            f"Followers: {user_info['followers']}\n"
            f"Following: {user_info['following']}\n"
            f"Public Repos Count: {user_info['public_repos']}\n"
            f"Bio: {user_info['bio']}\n"
        )
        self.user_info_window.setCentralWidget(self.centralwidget)

        self.user_info_window.show()

    def show_user_repos(self, user_repos):
        self.label = QtWidgets.QLabel(parent=self.user_info_window)
        self.label.setGeometry(QtCore.QRect(90, 200, 231, 32))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("User Repos:")
        for repo in user_repos:
            self.label.setText(f"{repo['name']}\n")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

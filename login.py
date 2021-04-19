from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * #QLabel, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem


class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        uic.loadUi('UI/login.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)


        self.show()


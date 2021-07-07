from PyQt5.QtWidgets import * #QLabel, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5 import uic, sip


class OnlineDialog(QDialog):
    open_chat = pyqtSignal(dict)

    def __init__(self, parent):
        super(OnlineDialog, self).__init__(parent)
        uic.loadUi('UI/onlineUI.ui', self)

        print(self.parent().online_users)
        self.online_listwidget.addItem("hahaha")
        self.online_listwidget.itemDoubleClicked.connect(self.openChat)
        

    @pyqtSlot(dict)
    def addOnlineUser(self, client):
        self.parent().online_users.update({client['username']: client})
        self.online_listwidget.clear()
        self.online_listwidget.addItems(self.parent().online_users.keys())

    def openChat(self, item):
        print(self.parent().online_users[item.text()])
        self.open_chat.emit(self.parent().online_users[item.text()])
        self.close()
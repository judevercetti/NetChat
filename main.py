from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from views import UI_Window
from cam import Camera
from network import Network, Client, Server
from MainUI import Ui_MainWindow
from CustomListViews import Messages
from TopBar import TitleBar
from login import LoginDialog

from qt_material import apply_stylesheet

# import threading


class NetCrawler(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainUI.ui", self)
        self.titlebar_layout.addWidget(TitleBar(self))


        self.messages = Messages(self)
        # network = Network()
        # network.startClient()
        # network.getMessage()

        self.thread = QThread()
        self.server = Server()
        self.server.moveToThread(self.thread)
        self.thread.started.connect(self.server.run)
        self.server.new_message.connect(self.messages.getMsg)
        self.thread.start()

        # self.show()
        self.login = LoginDialog()
        self.login.buttonBox.accepted.connect(self.setupApp)
        self.login.buttonBox.rejected.connect(qApp.quit)

    
    def setupApp(self):
        self.currentuser = self.login.username_lineedit.text()
        print(self.currentuser)
        self.show()



if __name__ == '__main__':

    camera = Camera(0)

    app = QApplication([])
    # start_window = UI_Window(camera)
    start_window = NetCrawler()
    
    # apply_stylesheet(app, theme='dark_teal.xml')

    # start_window.show()
    app.exit(app.exec_())
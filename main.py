from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, sip

from views import UI_Window
from cam import Camera
from network import NetFinder, Server
from CustomListViews import Messages
from dialogs import *
from TopBar import TitleBar
from login import LoginDialog

from qt_material import apply_stylesheet

import platform
import UI
# import threading


class NetCrawler(QMainWindow):
    current_user = {}
    online_users = {}

    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainUI.ui", self)
        self.titlebar_layout.addWidget(TitleBar(self))

        self.current_user['uid'] = platform.node()

        self.messages = Messages(self)
        
        #######################################     LOG IN      ###########################################
        self.login = LoginDialog()
        self.login.buttonBox.accepted.connect(self.setupApp)
        self.login.buttonBox.rejected.connect(qApp.quit)


        #######################################     SERVER      ###########################################
        # self.thread_server = QThread()
        # self.server = Server()
        # self.server.moveToThread(self.thread_server)
        # self.thread_server.started.connect(self.server.run)
        # self.server.new_message.connect(self.messages.getMsg)
        # self.thread_server.start()

        
        #######################################     ONLINE FINDER      ###########################################
        self.online_dialog = OnlineDialog(self)
        self.onlineusers_button.clicked.connect(self.online_dialog.show)
        self.online_dialog.open_chat.connect(self.messages.fillPaperList)


    
    def setupApp(self):
        self.current_user['username'] = self.login.username_lineedit.text()
        print(self.current_user['uid'])
        self.startNetFinder()
        self.show()


    def startNetFinder(self):
        self.thread_finder = QThread()
        self.online_finder = NetFinder(self.current_user)
        self.online_finder.moveToThread(self.thread_finder)
        self.thread_finder.started.connect(self.online_finder.run)
        self.online_finder.new_client.connect(self.online_dialog.addOnlineUser)
        self.thread_finder.start()



if __name__ == '__main__':

    camera = Camera(0)

    app = QApplication([])
    # start_window = UI_Window(camera)
    start_window = NetCrawler()
    
    # apply_stylesheet(app, theme='dark_teal.xml')

    # start_window.show()
    app.exit(app.exec_())
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from views import UI_Window
from cam import Camera

from MainUI import Ui_MainWindow
from custom_listview import exampleQMainWindow
from bar import TitleBar

from qt_material import apply_stylesheet


class NetCrawler(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.titlebar_layout.addWidget(TitleBar(self))

        exampleQMainWindow(self.chatroom_listwidget)


if __name__ == '__main__':

    camera = Camera(0)

    app = QApplication([])
    # start_window = UI_Window(camera)
    start_window = NetCrawler()
    
    apply_stylesheet(app, theme='dark_teal.xml')

    start_window.show()
    app.exit(app.exec_())
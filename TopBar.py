import sys
# from PyQt4 import QtGui
# from PyQt4 import QtCore
# from PyQt4.QtCore import Qt

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TitleBar(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.box = parent
        self.box.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAutoFillBackground(True)
        # self.setBackgroundRole(QPalette.Highlight)
        self.minimize=QPushButton(self)
        self.minimize.setIcon(QIcon('img/min.png'))
        self.maximize=QPushButton(self)
        self.maximize.setIcon(QIcon('img/max.png'))
        close=QPushButton(self)
        close.setIcon(QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label=QLabel(self)
        label.setText(self.box.windowTitle())
        self.setWindowTitle("Window Title")
        hbox=QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        self.box.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            self.box.showNormal()
            self.maxNormal= False
            self.maximize.setIcon(QIcon('img/max.png'))
            print ('1')
        else:
            self.box.showMaximized()
            self.maxNormal=  True
            print ('2')
            self.maximize.setIcon(QIcon('img/max2.png'))

    def close(self):
        self.box.close()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton and not self.maxNormal:
            self.box.moving = True
            self.box.offset = event.pos()

    def mouseMoveEvent(self,event):
        if not self.maxNormal:
            if self.box.moving: self.box.move(event.globalPos()-self.box.offset)


class Frame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.m_mouse_down= False
        self.setFrameShape(QFrame.StyledPanel)
        css = """
        QFrame{
            Background:  #D700D7
            color:white
            font:13px 
            font-weight:bold
            }
        """
        self.setStyleSheet(css) 
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= QWidget(self)
        vbox=QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        # vbox.setMargin(0)
        vbox.setSpacing(0)
        layout=QVBoxLayout(self)
        layout.addWidget(self.m_content)
        # layout.setMargin(5)
        layout.setSpacing(0)
        vbox.addLayout(layout)
        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button()== Qt.LeftButton

    def mouseMoveEvent(self,event):
        x=event.x()
        y=event.y()

    def mouseReleaseEvent(self,event):
        m_mouse_down=False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = Frame()
    box.move(60,60)
    box.show()
    app.exec_()
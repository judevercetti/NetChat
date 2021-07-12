from dialogs import OnlineDialog
from PyQt5.QtWidgets import * #QLabel, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem
from PyQt5.QtGui import *
from PyQt5 import QtCore, uic, sip
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import time


allmessages = {
    "y545trsg": [
        {
            "content": "hi",
            "time": 1625633425.7058942,
            "sender": "y545trsg",
            "receiver": "kagwa69"
        },
        {
            "content": "oh hello, wats gud",
            "time": 1625633425.7058942,
            "sender": "kagwa69",
            "receiver": "y545trsg"
        }
    ],
    "rn35kjn": [
        {
            "content": "whats gud bwoy",
            "time": 1625633425.7058942,
            "sender": "rn35kjn",
            "receiver": "kagwa69"
        }
    ],
    "pronto": [
        {
            "content": "Ogamba chi",
            "time": 1625633425.7058942,
            "sender": "pronto",
            "receiver": "kagwa69"
        }
    ]
}

  
class PaperStream(QObject):
    change_text = pyqtSignal(str)
    is_loading = pyqtSignal(bool)
    fill_paper_list = pyqtSignal(dict)

    def __init__(self):
        super(PaperStream, self).__init__()
        # db = firestore.client()
        self.docs = [
            {
                "id": "y545trsg",
                "username": "kagwa",
                "last_message": "oi oi oi matte"
            },
            {
                "id": "rn35kjn",
                "username": "mundo",
                "last_message": "wallo maria"
            }
        ]

        # users_ref = db.collection(u'papers')
        # self.docs = users_ref.stream()


    def run(self):
        for doc in self.docs:
            # new_doc.update({'id': doc.id})
            self.fill_paper_list.emit(doc)


class PapersListwidget(QWidget):
    def __init__(self, paper):
        super().__init__()
        self.align_layout = QHBoxLayout()
        self.msg_layout = QVBoxLayout()
        self.paper_id = paper['id']
        # self.paper_text = paper['content']
        self.paper_type_label = QLabel(f'{paper["username"]}')
        self.paper_form_label = QLabel(f'{paper["last_message"]}')

        self.msg_layout.addWidget(self.paper_type_label)
        self.msg_layout.addWidget(self.paper_form_label)
        self.align_layout.addLayout(self.msg_layout)
        self.setLayout(self.align_layout)


class Messages(QWidget):
    current_paper_id = None

    def __init__ (self, parent):
        super(Messages, self).__init__(parent)
        self.myQListWidget = self.parent().users_listwidget # QListWidget(self)
        self.paper_content = self.parent().chatroom_listwidget
        self.myQListWidget.itemClicked.connect(self.setCurrentPaper)

        self.parent().mymsg_textEdit.textChanged.connect(self.checkMessage)
        self.parent().sendmsg_button.clicked.connect(self.sendMessage)


        self.thread = QThread()
        self.worker = PaperStream()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.change_text.connect(self.mans)
        self.worker.is_loading.connect(self.setLoader)
        self.worker.fill_paper_list.connect(self.fillPaperList)
        self.thread.start()


    @pyqtSlot(dict)
    def fillPaperList(self, paper):
        myQCustomQWidget = PapersListwidget(paper)
        myQListWidgetItem = QListWidgetItem(self.myQListWidget)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

        self.myQListWidget.addItem(myQListWidgetItem)
        self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        myQListWidgetItem.setData(QtCore.Qt.UserRole, myQCustomQWidget)

    def setCurrentPaper(self, item):
        myobj = item.data(QtCore.Qt.UserRole)
        if self.current_paper_id == myobj.paper_id: return
        
        self.paper_content.clear()
        self.current_paper_id = myobj.paper_id

        self.parent().username_label.setText(myobj.paper_type_label.text())

        try:
            for mymsg in allmessages[self.current_paper_id]:
                self.userMessageList(mymsg)
        except:
            print("no msgs")

    def userMessageList(self, mymsg):
            myQCustomQWidget = ChatRoomListWidget(mymsg['content'], mymsg['time'], mymsg['sender'], self.parent().current_user['uid'])
            myQListWidgetItem = QListWidgetItem(self.paper_content)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.paper_content.addItem(myQListWidgetItem)
            self.paper_content.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def sendMessage(self):
        msg = {
            "content": self.parent().mymsg_textEdit.toPlainText(),
            "time": time.time(),
            "sender": self.parent().current_user['uid'],
            "receiver": self.current_paper_id
        }
        allmessages[self.current_paper_id].append(msg)
        self.userMessageList(msg)

    def checkMessage(self, txt):
        self.parent().sendmsg_button.setEnabled(True if len(str.strip(txt)) > 0 else False)

    @pyqtSlot(str)
    def mans(self, txt):
        print(f"thread man dem {txt}")

    @pyqtSlot(bool)
    def setLoader(self, isLoading):
        print("whats this")

    def createPaper(self):
        print("paper created")
        self.online_dialog = OnlineDialog()
        self.online_dialog.online_listwidget.addItem("hahaha")

    
    @pyqtSlot(dict)
    def getMsg(self, msg):
        allmessages[msg['id']].append(msg)
        if msg['id'] == self.current_paper_id:
            self.userMessageList(msg)


class AddPaper(QDialog):
    def __init__(self):
        super(AddPaper, self).__init__()
        uic.loadUi('UI/addpaper.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.buttonBox.accepted.connect(lambda: self.uploadPaper(
            self.type_linedit.text(),
            self.form_combobox.currentIndex() + 1,
            self.subject_combobox.currentText(),
            self.year_linedit.text(),
            self.content_textedit.toPlainText()
        ))
        self.show()



class ChatRoomListWidget(QWidget):
    def __init__(self, msgtext, msgtime, msgsender, currentuser):
        super().__init__()
        self.align_layout = QHBoxLayout()
        self.msg_layout = QVBoxLayout()
        self.msg_text = QLabel(msgtext)
                
        t = time.localtime(msgtime)
        msgtime = time.strftime("%I:%M %p", t)
        self.msg_time = QLabel(msgtime)

        if msgsender == currentuser:
            self.align_layout.addStretch(1)
            self.msg_text.setAlignment(QtCore.Qt.AlignRight)
            self.msg_time.setAlignment(QtCore.Qt.AlignRight)

        self.msg_layout.addWidget(self.msg_text)
        self.msg_layout.addWidget(self.msg_time)
        self.align_layout.addLayout(self.msg_layout)
        self.setLayout(self.align_layout)


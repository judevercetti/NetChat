import cv2
import zmq
import base64
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Network(QObject):
    def __init__(self):
        super(Network, self).__init__()
        print("network started")
        self.ip = '127.0.0.1'
        
        self.context = zmq.Context()

    def startServer(self):
        self.server = self.context.socket(zmq.PUB)
        self.server.bind('tcp://*:5555')
        print('server started')

    def startClient(self):
        self.client = self.context.socket(zmq.SUB)
        self.client.connect('tcp://127.0.0.1:5555')
        self.client.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    def getMessage(self):
        while True:
            try:
                msg = self.client.recv_string()
                print(f'msg >> {msg}')

            except KeyboardInterrupt:
                print("server closed")
                break



class Server(QObject):
    new_message = pyqtSignal(dict)

    def __init__(self):
        super(Server, self).__init__()

        self.context = zmq.Context()
        self.server = self.context.socket(zmq.REP)
        self.server.bind('tcp://*:5555')
        print('server started')


    def run(self):
        print('server ready to receive')
        while True:
            try:
                msg = self.server.recv_json()
                print(f'msg>> {msg}')
                self.new_message.emit(msg)
                self.server.send_string('received msg')

            except KeyboardInterrupt:
                print("client closed")
                break









class Client(QObject):
    new_message = pyqtSignal(dict)

    def __init__(self):
        super(Client, self).__init__()

        self.context = zmq.Context()
        self.client = self.context.socket(zmq.SUB)
        self.client.connect('tcp://127.0.0.1:5555')
        self.client.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    def run(self):
        print('client ready to receive')
        while True:
            try:
                msg = self.client.recv_json()
                print(f'msg>> {msg}')
                self.new_message.emit(msg)

            except KeyboardInterrupt:
                print("client closed")
                break

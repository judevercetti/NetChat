import cv2
import zmq
import base64
import numpy as np
import time
import socket
import struct
import json

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


my_ip = socket.gethostbyname(socket.gethostname())

class Server(QObject):
    new_message = pyqtSignal(dict)

    def __init__(self):
        super(Server, self).__init__()

        self.context = zmq.Context()
        self.server = self.context.socket(zmq.REP)
        self.server.bind('tcp://*:98652')
        # print('server started')


    def run(self):
        # print('server ready to receive')
        while True:
            try:
                msg = self.server.recv_json()
                print(f'msg>> {msg}')
                self.new_message.emit(msg)
                self.server.send_string('received msg')

            except KeyboardInterrupt:
                print("client closed")
                break









# class Client(QObject):
#     new_message = pyqtSignal(dict)

#     def __init__(self):
#         super(Client, self).__init__()

#         self.context = zmq.Context()
#         self.client = self.context.socket(zmq.SUB)
#         self.client.connect('tcp://127.0.0.1:5555')
#         self.client.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

#     def run(self):
#         print('client ready to receive')
#         while True:
#             try:
#                 msg = self.client.recv_json()
#                 print(f'msg>> {msg}')
#                 self.new_message.emit(msg)

#             except KeyboardInterrupt:
#                 print("client closed")
#                 break



class OnlineFinder(QObject):
    new_client = pyqtSignal(dict)

    def __init__(self):
        super(OnlineFinder, self).__init__()

        self.context = zmq.Context()
        self.finder = self.context.socket(zmq.SUB)
        self.finder.connect(f'tcp://10.119.6.51:99652')
        self.finder.subscribe("")
        print('online finder started')

        self.advertiser = self.context.socket(zmq.PUB)
        self.advertiser.bind('tcp://*:99652')
        print('online advertiser started')


    def run(self):
        print('online finder ready to receive')
        time.sleep(1)
        self.advertiser.send_json({
            'username': socket.gethostname()
        })
        while True:
            try:
                msg = self.finder.recv_json()
                print(f'online >> {msg}')
                self.new_client.emit(msg)
                # self.finder.send_string('received msg')

            except KeyboardInterrupt:
                print("online finder closed")


class NetFinder(QObject):
    new_client = pyqtSignal(dict)

    def __init__(self):
        super(NetFinder, self).__init__()

        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        IS_ALL_GROUPS = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.sock.bind(('', MCAST_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            self.sock.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


    def run(self):
        while True:
            new_client_msg = self.sock.recv(10240)
            print(new_client_msg)
            self.new_client.emit(json.loads(new_client_msg.decode()))


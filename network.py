import socket
import threading
class Network:
    def __init__(self, ip='192.168.0.113', port=5555, ENC_FORMAT = 'UTF-8'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.player = self.connect()
        self.ENC_FORMAT = ENC_FORMAT

    def getInitialData(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error:
            pass

    def receive(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


    def send(self, data):
        try:
            self.client.send(data.encode(self.ENC_FORMAT))
            # return self.client.recv(2048).decode(self.ENC_FORMAT)
        except socket.error as e:
            print(e)

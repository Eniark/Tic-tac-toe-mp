import socket

class Network:
    def __init__(self, ip, port, ENC_FORMAT = 'UTF-8'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.__first_connection = self.connect()
        self.ENC_FORMAT = ENC_FORMAT

    def getPl(self):
        return self.__first_connection

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048)
        except socket.error:
            pass

    def send(self, data: str):
        try:
            self.client.send(data.encode(self.ENC_FORMAT))
            return self.client.recv(2048).decode(self.ENC_FORMAT)
        except socket.error:
            pass

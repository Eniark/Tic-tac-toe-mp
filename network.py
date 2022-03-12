import socket

# class for easier client-socket communication
class Network:
    def __init__(self, ip, port=5555, ENC_FORMAT = 'UTF-8'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.player = self.connect()
        self.ENC_FORMAT = ENC_FORMAT

    def getInitialData(self):
        """
        First call to server. Get player (X or O)
        """
        return self.player

    def connect(self):
        """
        Connect and receive something from server
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def receive(self):
        """
        Listen for data from server
        """
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


    def send(self, data):
        """
        :param data: data be sent
        Sending data to server
        """
        try:
            self.client.send(data.encode(self.ENC_FORMAT))
        except socket.error as e:
            print(e)

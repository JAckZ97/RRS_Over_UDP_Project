import socket

class Client:
    
    def __init__(self):
        self.HOST = 'localhost' 
        self.PORT = 8888   
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      

    def listenMsg(self):
        data, addr = self.clientSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg):
        self.clientSocket.sendto(msg, (self.HOST, self.PORT))

    def run(self):
        while True:
            data, addr = listenMsg()

            '''
            switch data:
            
                do things

            '''

import socket
from message_db import Message, MessageController, MessageTypes

class Client:
    
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 8888   
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.msgControl = MessageController()

    def listenMsg(self):
        data, addr = self.clientSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg):
        self.clientSocket.sendto(msg, (self.HOST, self.PORT))

    def run(self):
        while True:
            # data, addr = listenMsg()

            message = input("msg (q to quit): ")
            if message == "q":
                break

            elif message == "s":
                message = Message(MessageTypes.SUBJECTS, rqNum = 1, name = "Jack", subjects = ["ps5", "spiderman"])
                self.sendMsg(self.msgControl.serialize(message))

            else:
                print("invalid")

cl = Client()
cl.run()

# FIXME : Client need to connect to the appropriate server

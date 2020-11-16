import socket
from message_db import Message, MessageController, MessageTypes
from database import DatabaseController

class Server:

    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 8888   
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((self.HOST, self.PORT))
        self.msgControl = MessageController()
        self.dbControl = DatabaseController()

        self.messageFunctions = {
            MessageTypes.SUBJECTS: self.request_subjectInt_update,
            MessageTypes.SUBJECTS_UPDATED: self.accept_subjectInt_update
        }

    # Message Functions
    def request_subjectInt_update(self, message):
        self.dbControl.editUserData(1, DatabaseController.User.UserDataType.SUBJECT_INTEREST, message.subjects)

    def accept_subjectInt_update(self, message):
        pass

    # Class functions
    def listenMsg(self):
        data, addr = self.serverSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg):
        self.serverSocket.sendto(msg, (self.HOST, self.PORT))

    def run(self):
        while True:
            data, addr = self.listenMsg()
            message = self.msgControl.deserialize(data)
            self.messageFunctions[message.type_](message)

ser = Server()
ser.run()

import socket
import threading
from message_db import Message, MessageController, MessageTypes
from database import DatabaseController

class Server:

    def __init__(self, name, host = 'localhost', port = 8888):
        self.name = name
        self.HOST = host
        self.PORT = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((self.HOST, self.PORT))
        self.msgControl = MessageController()
        self.dbControl = DatabaseController()

        self.messageFunctions = {
            MessageTypes.SUBJECTS: self.request_subjectInt_update,
            MessageTypes.SUBJECTS_UPDATED: self.accept_subjectInt_update,
            MessageTypes.REGISTER: self.register_client
        }

        self.stopFlag = False

        self.serverSocket.settimeout(2) # un-block after 2s


    # Message Functions
    def request_subjectInt_update(self, message):
        self.dbControl.editUserData(1, DatabaseController.User.UserDataType.SUBJECT_INTEREST, message.subjects)

    def accept_subjectInt_update(self, message):
        pass

    def register_client(self, clientMessage):
        print("server is registering client")
        msg = Message(type_ = MessageTypes.REGISTERED, rqNum = clientMessage.rqNum)

        self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

    # Class functions
    def listenMsg(self):
        data, addr = self.serverSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg, host, port):
        self.serverSocket.sendto(msg, (host, port)) # FIXME : needs to be server host, port no ?

    def pause(self):
        print("pausing server -> ", self.name)
        self.stopFlag = True

    def closeServer(self):
        self.serverSocket.shutdown(socket.SHUT_RDWR)
        self.serverSocket.close()

    def run(self):
        # reset flag
        self.stopFlag = False

        print("running server -> ", self.name)
        while not self.stopFlag:
            try:
                data, addr = self.listenMsg()
                message = self.msgControl.deserialize(data)
                self.messageFunctions[message.type_](message)

            except socket.timeout:
                print("server time out")

            # FIXME : problem is that we cannot close the server, when it is waiting in the listenMsg() function (its blocking)

    def start(self):
        serverThread = threading.Thread(target=self.run)
        serverThread.start()

        # NOTE : in theory, the thread ends when we "pause" the server, so dont need thread.join() ?

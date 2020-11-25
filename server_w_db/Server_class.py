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
            MessageTypes.REGISTER: self.register_client,
            MessageTypes.DEREGISTER: self.deregister_client,
            MessageTypes.UPDATE: self.update_user_socket_info

            # MessageTypes.SUBJECTS: self.request_subjectInt_update,
            # MessageTypes.SUBJECTS_UPDATED: self.accept_subjectInt_update,
        }

        self.stopFlag = False
        self.serverSocket.settimeout(2) # un-block after 2s

    # Message Functions
    # def request_subjectInt_update(self, message):
    #     self.dbControl.editUserData(1, DatabaseController.User.UserDataType.SUBJECT_INTEREST, message.subjects)

    def register_client(self, clientMessage):
        user = DatabaseController.User(clientMessage.name, clientMessage.host, False, clientMessage.port, "")
        accept = self.dbControl.addUser(user)

        if accept:
            print("server " + self.name + " is deregistering client " + clientMessage.name)
            msg = Message(type_ = MessageTypes.DEREGISTER, rqNum = clientMessage.rqNum)

            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

        else:
            print("server " + self.name + " denied deregistering client " + clientMessage.name)
            msg = Message(type_ = MessageTypes.REGISTER_DENIED, rqNum = clientMessage.rqNum, reason = "user exists already")

            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)


    def deregister_client(self, clientMessage):
        accept = self.dbControl.deleteUser(clientMessage.name)

        if accept:
            # TODO : send message to other server
            pass

        else:
            pass


    def update_user_socket_info(self, clientMessage):
        resultA = self.dbControl.editUserData(clientMessage.name, DatabaseController.User.UserDataType.IP_ADDRESS, clientMessage.ipAddress)
        resultB = self.dbControl.editUserData(clientMessage.name, DatabaseController.User.UserDataType.SOCKET_NUMBER, clientMessage.socketNum)
        
        if resultA == True and resultB == True:
            print("server " + self.name + " update client ip_address and port number " + clientMessage.name)

            msg = Message(type_ = MessageTypes.UPDATE_CONFIRMED, rqNum = clientMessage.rqNum, name = clientMessage.name, ipAddress = clientMessage.ipAddress, socketNum = clientMessage.socketNum)
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)
            
        else:
            print("server " + self.name + " denied update client ip_address and port number " + clientMessage.name)
            msg = Message(type_ = MessageTypes.UPDATE_DENIED, rqNum = clientMessage.rqNum, reason = " name is not in database")
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
                # print("server time out")
                pass

            # FIXME : problem is that we cannot close the server, when it is waiting in the listenMsg() function (its blocking)

    def start(self):
        serverThread = threading.Thread(target=self.run)
        serverThread.start()

        # NOTE : in theory, the thread ends when we "pause" the server, so dont need thread.join() ?

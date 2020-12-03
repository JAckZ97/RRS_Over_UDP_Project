import select
import socket
import threading
from message_db import Message, MessageController, MessageTypes
from database import DatabaseController

class Server:

    def __init__(self, name, host = 'localhost', port = 8888, databaseFilePath = ""):
        self.name = name
        self.HOST = host
        self.PORT = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.otherServer = None

        # FIXME : here we are basically saying we are listening only to self.HOST network address
        self.serverSocket.bind((self.HOST, self.PORT))
        self.msgControl = MessageController()
        self.dbControl = DatabaseController(databaseFilePath)

        self.messageFunctions = {
            MessageTypes.REGISTER: self.register_client,
            MessageTypes.DEREGISTER: self.deregister_client,
            MessageTypes.UPDATE: self.update_user_socket_info,
            MessageTypes.SUBJECTS: self.update_user_subject_interest,
            MessageTypes.PUBLISH: self.request_publish,
            MessageTypes.PING: self.ping_test,

            MessageTypes.REGISTERED: self.register_client_paused,
            MessageTypes.REGISTER_DENIED: self.register_denied_paused,
            MessageTypes.DEREGISTERED: self.deregister_client_paused,
            MessageTypes.SUBJECTS_UPDATED: self.update_user_subject_interest_paused
        }

        self.listenClient = True
        self.stopFlag = False
        self.serverSocket.settimeout(0.1) # un-block after 2s

        # List of Possible Subjects
        self.subjectOfInterests = ["ps", "xbox", "pc", "nintendo", "vr"]

    def set_otherServer(self, otherServer):
        self.otherServer = otherServer

    # Message Functions
    def ping_test(self, clientMessage):
        print("server " + self.name + " ping test client " + clientMessage.name)
        msg = Message(type_ = MessageTypes.PING, text = self.name)
        self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

    def register_client(self, clientMessage):
        user = DatabaseController.User(clientMessage.name, clientMessage.host, False, clientMessage.port, "", "")
        accept = self.dbControl.addUser(user)

        if accept:
            print("server " + self.name + " is registering client " + clientMessage.name)

            # send to client
            msg = Message(type_ = MessageTypes.REGISTERED, rqNum = clientMessage.rqNum)
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

            # send to other server
            msg = Message(type_ = MessageTypes.REGISTERED, name=clientMessage.name, host=clientMessage.host, port=clientMessage.port, isServer=True)
            self.sendMsg(self.msgControl.serialize(msg), self.otherServer.HOST, self.otherServer.PORT)

        else:
            print("server " + self.name + " denied registering client " + clientMessage.name)
            # send to client
            msg = Message(type_ = MessageTypes.REGISTER_DENIED, rqNum = clientMessage.rqNum, reason = "user exists already")
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

            # send to other server
            msg = Message(type_ = MessageTypes.REGISTER_DENIED, name = clientMessage.name, isServer=True)
            self.sendMsg(self.msgControl.serialize(msg), self.otherServer.HOST, self.otherServer.PORT)

    def register_client_paused(self, clientMessage):
        print("server " + self.name + " ack. register for client " + clientMessage.name)
        user = DatabaseController.User(clientMessage.name, clientMessage.host, False, clientMessage.port, "", "")
        accept = self.dbControl.addUser(user)

    def register_denied_paused(self, clientMessage):
        print("server " + self.name + " ack. register denied for client " + clientMessage.name)

    def deregister_client_paused(self, clientMessage):
        print("server " + self.name + " ack. deregister for client " + clientMessage.name)
        accept = self.dbControl.deleteUser(clientMessage.name)

    def update_user_subject_interest_paused(self, clientMessage):
        print("server " + self.name + " ack. subject update for client " + clientMessage.name)
        self.dbControl.editUserData(clientMessage.name, DatabaseController.User.UserDataType.SUBJECT_INTEREST, clientMessage.subjects)

    def deregister_client(self, clientMessage):
        accept = self.dbControl.deleteUser(clientMessage.name)

        if accept:
            # TODO : send message to other server
            # send to other server
            msg = Message(type_ = MessageTypes.DEREGISTERED, name = clientMessage.name, isServer=True)
            self.sendMsg(self.msgControl.serialize(msg), self.otherServer.HOST, self.otherServer.PORT)

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


    def update_user_subject_interest(self, clientMessage):
        
        nameExistFlag = False
        if self.dbControl.checkExistUser(clientMessage.name):
            nameExistFlag = True

        denyFlag = False
        # check if subject given by client is available
        for val in clientMessage.subjects:
            if val not in self.subjectOfInterests:
                denyFlag = True

        if not denyFlag and nameExistFlag:
            print("server " + self.name + " update subject of interest " + clientMessage.name)
            msg = Message(type_ = MessageTypes.SUBJECTS_UPDATED, rqNum = clientMessage.rqNum, name = clientMessage.name, subjects = clientMessage.subjects)
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)
            self.dbControl.editUserData(clientMessage.name, DatabaseController.User.UserDataType.SUBJECT_INTEREST, clientMessage.subjects)

            # send to other server
            msg = Message(type_ = MessageTypes.SUBJECTS_UPDATED, rqNum = clientMessage.rqNum, name = clientMessage.name, subjects = clientMessage.subjects, isServer=True)
            self.sendMsg(self.msgControl.serialize(msg), self.otherServer.HOST, self.otherServer.PORT)

        elif denyFlag and not nameExistFlag:
            print("server " + self.name + " reject update subject of interest " + clientMessage.name)
            msg = Message(type_ = MessageTypes.SUBJECTS_REJECTED, rqNum = clientMessage.rqNum, name = clientMessage.name, reason = " At least one subject is not in database and the user is not registered")
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

        elif not denyFlag and not nameExistFlag:
            print("server " + self.name + " reject update subject of interest " + clientMessage.name)
            msg = Message(type_ = MessageTypes.SUBJECTS_REJECTED, rqNum = clientMessage.rqNum, name = clientMessage.name, reason = " User is not registered in the database")
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

        else:
            print("server " + self.name + " reject update subject of interest " + clientMessage.name)
            msg = Message(type_ = MessageTypes.SUBJECTS_REJECTED, rqNum = clientMessage.rqNum, name = clientMessage.name, reason = " At least one subject is not in database")
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

    def request_publish(self, clientMessage):

        if self.dbControl.checkExistUser(clientMessage.name):
            if clientMessage.subjects[0] in self.subjectOfInterests: # assuming only 1 subject passed

                # add news to database SOI
                self.dbControl.addMessage(clientMessage.subjects[0], clientMessage.text)

                # send messages to users
                usersNames = self.dbControl.get_existing_users()
                for userName in usersNames:
                    userSOIs = self.dbControl.readOneData(userName, DatabaseController.User.UserDataType.SUBJECT_INTEREST)
                    userHost = self.dbControl.readOneData(userName, DatabaseController.User.UserDataType.IP_ADDRESS)
                    userPort = self.dbControl.readOneData(userName, DatabaseController.User.UserDataType.SOCKET_NUMBER) # FIXME -> not sure if it returns an int
                    if clientMessage.subjects[0] in userSOIs:
                        print("server " + self.name + " message news " + userName)
                        msg = Message(type_ = MessageTypes.MESSAGE, name = userName, subjects =  clientMessage.subjects[0], text = clientMessage.text)
                        self.sendMsg(self.msgControl.serialize(msg), userHost, userPort)

            else:
                # send to message user that it was denied
                print("server " + self.name + " reject publish news " + clientMessage.name)
                msg = Message(type_ = MessageTypes.PUBLISH_DENIED, rqNum = clientMessage.rqNum, reason = "subject is not in database")
                self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

        else:
            # send to message user that it was denied
            print("server " + self.name + " reject publish news " + clientMessage.name)
            msg = Message(type_ = MessageTypes.PUBLISH_DENIED, rqNum = clientMessage.rqNum, reason = "user is not registered in the database")
            self.sendMsg(self.msgControl.serialize(msg), clientMessage.host, clientMessage.port)

    # Class functions
    def server_switch_msg(self, newServer):
        # send to message user that it was denied
        print("server " + self.name + " switch to " + newServer.name)
        
        # FIXME : here we need to check if the users are connected before we send a message to them !!! or else will have error
        # however, the error is only seen on WINDOWS
        # send messages to users
        usersNames = self.dbControl.get_existing_users()
        for userName in usersNames:
            userHost = self.dbControl.readOneData(userName, DatabaseController.User.UserDataType.IP_ADDRESS)
            userPort = self.dbControl.readOneData(userName, DatabaseController.User.UserDataType.SOCKET_NUMBER) # FIXME -> not sure if it returns an int
            msg = Message(type_ = MessageTypes.CHANGE_SERVER, ipAddress = newServer.HOST, socketNum = newServer.PORT)
            self.sendMsg(self.msgControl.serialize(msg), userHost, userPort)

    def listenMsg(self):
        data, addr = self.serverSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg, host, port):
        self.serverSocket.sendto(msg, (host, port)) # FIXME : needs to be server host, port no ?

    def pause(self):
        print("pausing server -> ", self.name)
        # self.stopFlag = True
        self.listenClient = False

    def closeServer(self):
        self.serverSocket.shutdown(socket.SHUT_RDWR)
        self.serverSocket.close()

    def run(self):
        # reset flag
        self.stopFlag = False
        self.listenClient = True
        print("running server -> ", self.name)
        while not self.stopFlag:
            try:
                data, addr = self.listenMsg()
                message = self.msgControl.deserialize(data)
                
                # check if message is from client or server
                if (message.isServer == False) and self.listenClient == False:
                    pass
                else:
                    self.messageFunctions[message.type_](message)

            except socket.timeout:
                # print("server time out")
                pass

            # FIXME : problem is that we cannot close the server, when it is waiting in the listenMsg() function (its blocking)

    def start(self):
        # FIXME : the problem is that when a server gets reconnected, it will listenMsg to any msg in the input buffer
        # -> therefore, we need to empty the socket.
        # -> the below function seems to be working, but if we do it at a "tipping" point, when its switching server,
        # -> both servers receives it
        # NOTE : after some more trial/error -> it seems the source of the problem why sometimes the two servers were responding is because of the "timeout"
        # -> the timeout is actually preventing the server to "close" for x amount of seconds, therefore
        # -> there is a small gap time, where actually both servers are listening and active (gap time == timeout)
        # self.empty_socket(self.serverSocket)
        self.clear_buffer(self.serverSocket)

        serverThread = threading.Thread(target=self.run)
        serverThread.start()

        # NOTE : in theory, the thread ends when we "pause" the server, so dont need thread.join() ?

    # NOTE : 2 different ways to empty input buffer
    def empty_socket(self, sock):
        # https://stackoverflow.com/questions/1097974/how-to-empty-a-socket-in-python
        """remove the data present on the socket"""
        input = [sock]
        while 1:
            inputready, o, e = select.select(input,[],[], 0.0)
            if len(inputready)==0: break
            for s in inputready: s.recv(1)

    def clear_buffer(self, sock):
        try:
            while sock.recv(1024): pass
        except:
            pass

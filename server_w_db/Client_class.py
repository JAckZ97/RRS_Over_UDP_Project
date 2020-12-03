import socket
import threading
import time
from message_db import Message, MessageController, MessageTypes
from globals_ import serverAHost, serverAPort, serverBHost, serverBPort

class Client:
    
    def __init__(self, name, host = 'localhost', port = 8888):
        self.name = name
        self.HOST = host
        self.PORT = port   
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.bind((self.HOST, self.PORT))
        self.msgControl = MessageController()

        self.messageFunctions = {
            MessageTypes.REGISTERED: self.print_registered,
            MessageTypes.REGISTER_DENIED: self.print_registered_denied,
            MessageTypes.UPDATE_CONFIRMED: self.print_updated_socket_info,
            MessageTypes.UPDATE_DENIED: self.print_updated_socket_info_denied,
            MessageTypes.SUBJECTS_UPDATED:self.print_updated_soi,
            MessageTypes.SUBJECTS_REJECTED:self.print_updated_soi_denied,
            MessageTypes.MESSAGE:self.print_publish_message,
            MessageTypes.PUBLISH_DENIED:self.print_publish_denied,
            MessageTypes.CHANGE_SERVER: self.switch_server,
            MessageTypes.PING: self.ping_test
        }

        self.serverHost = ""
        self.serverPort = 0

        self.stopListenFlag = False

        self.clientSocket.settimeout(1) # un-block after 1s

    # Message Functions
    def ping_test(self, message):
        print("PING test succeed with server " + message.text)

    def switch_server(self, message):

        # stop listening
        self.stopListenFlag = True

        self.serverHost = message.ipAddress
        self.serverPort = message.socketNum

        # resume listening
        self.stopListenFlag = False

    def print_registered(self, message):
        print("I " + self.name + " is registered !")

    def print_updated_socket_info(self, message):
        print("I " + self.name + " is updated !")

    def print_registered_denied(self, message):
        print("I " + self.name + " is registered denied !")

    def print_updated_socket_info_denied(self, message):
        print("I " + self.name + " is updated denied !")

    def print_updated_soi(self, message):
        print("I " + self.name + " SOI is updated !")

    def print_updated_soi_denied(self, message):
        print("I " + self.name + " SOI is denied !")
        print(message.reason)

    def print_publish_message(self, message):
        print("I " + self.name + " receive message " + message.text)

    def print_publish_denied(self, message):
        print("I " + self.name + " publish is denied !")
        print(message.reason)

    # Class Functions
    def listenMsg(self):
        data, addr = self.clientSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg):
        self.clientSocket.sendto(msg, (self.serverHost, self.serverPort)) # FIXME : needs to be server host, port no ?
    
    def sendRegisterMsg(self, msg):
        # send to both servers
        self.clientSocket.sendto(msg, (serverAHost, serverAPort)) # FIXME : needs to be server host, port no ?
        self.clientSocket.sendto(msg, (serverBHost, serverBPort)) # FIXME : needs to be server host, port no ?

    def update_host_port(self):
        # FIXME : since timeout 1s, there is a possbility that we are listenMsg + bind at the same time == ERROR

        # stop listening
        self.stopListenFlag = True

        self.HOST = input("host : ")
        self.PORT = int(input("port : "))

        # NOTE : Need to close and make a new socket before updating new ip address and port
        # close socket
        self.clientSocket.shutdown(socket.SHUT_RD)
        self.clientSocket.close()

        # create new socket
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.bind((self.HOST, self.PORT))

        # resume listening
        self.stopListenFlag = False
    
    def set_server(self, host, port):
        self.serverHost = host
        self.serverPort = port

    def run(self):
        msgThread = threading.Thread(target=self.msg_thread)
        msgThread.start()

        listenThread = threading.Thread(target=self.listen_thread)
        listenThread.start()

    def msg_thread(self):
        options = ["register", "update", "deregister", "subject", "publish", "ping"]
        print("here are the options : ", options)

        while True:
            # data, addr = listenMsg()

            message = input("msg (q to quit) : ")

            if message == MessageTypes.REGISTER.value:
                
                msg = Message(type_ = MessageTypes.REGISTER, rqNum = 1, name = self.name, 
                    ipAddress = self.HOST, socketNum = self.PORT, host = self.HOST, port = self.PORT)

                self.sendRegisterMsg(self.msgControl.serialize(msg))
                
            elif message == MessageTypes.UPDATE.value:
                
                # update host and port
                self.update_host_port()
                
                msg = Message(type_ = MessageTypes.UPDATE, rqNum = 1, name = self.name, 
                    ipAddress = self.HOST, socketNum = self.PORT, host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

            elif message == MessageTypes.DEREGISTER.value:
                
                msg = Message(type_ = MessageTypes.DEREGISTER, rqNum = 1, name = self.name, host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

            elif message == MessageTypes.SUBJECTS.value:
                print(["ps", "xbox", "pc", "nintendo", "vr"])
                subjects = input(" subcribe to ? (put space in between) : ")
                subjects = subjects.split()
    
                msg = Message(type_ = MessageTypes.SUBJECTS, rqNum = 1, name = self.name, subjects = subjects, host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

            elif message == MessageTypes.PUBLISH.value:
                print("What subject do you want to publish on:")
                print(["ps", "xbox", "pc", "nintendo", "vr"])
                subjects = input("Subject: ")
                subjects = subjects.split()

                if len(subjects) > 1:
                    print("too many subjects")

                else:
                    print("What do you want to publish")
                    news = input("News: ")
                    msg = Message(type_ = MessageTypes.PUBLISH, rqNum = 1, name = self.name, subjects = subjects, text = news,  host = self.HOST, port = self.PORT)

                    self.sendMsg(self.msgControl.serialize(msg))

            elif message == MessageTypes.PING.value:
                print("PING sent")
                msg = Message(type_ = MessageTypes.PING, rqNum = 1, name = self.name, host = self.HOST, port = self.PORT)
                self.sendMsg(self.msgControl.serialize(msg))
                
            else:
                print("invalid choice")
                
    def listen_thread(self):
        while True:
            if not self.stopListenFlag:
                try:
                    data, addr = self.listenMsg()
                    message = self.msgControl.deserialize(data)
                    self.messageFunctions[message.type_](message)

                    # FIXME : just to make printing pretty
                    print("")

                except socket.timeout:
                    # print("server time out")
                    pass
            
            else:
                time.sleep(0.001)
            
# FIXME : Client need to connect to the appropriate server

    

import socket
import threading
from message_db import Message, MessageController, MessageTypes

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
        }

        self.serverHost = ""
        self.serverPort = 0

    # Message Functions
    def print_registered(self, message):
        print("I " + self.name + "is registered !")

    # Class Functions
    def listenMsg(self):
        data, addr = self.clientSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg):
        self.clientSocket.sendto(msg, (self.serverHost, self.serverPort)) # FIXME : needs to be server host, port no ?

    def set_server(self, host, port):
        self.serverHost = host
        self.serverPort = port

    def run(self):
        msgThread = threading.Thread(target=self.msg_thread)
        msgThread.start()

        listenThread = threading.Thread(target=self.listen_thread)
        listenThread.start()

    def msg_thread(self):
        while True:
            # data, addr = listenMsg()

            message = input("msg (q to quit): ")
            messageList = message.split()

            if messageList[0] == MessageTypes.REGISTER.value:
                print("Client_Name - IP_address - Socket_Number")
                
                # msgList = {
                #         'Client_Name': messageList[1], 
                #         'IP_address': messageList[2], 
                #         'Socket_Number': int(messageList[3])
                #     }

                msg = Message(type_ = MessageTypes.REGISTER, rqNum = 1, name = messageList[1], 
                    ipAddress = messageList[2], socketNum = int(messageList[3]), host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

    def listen_thread(self):
        while True:
            data, addr = self.listenMsg()
            message = self.msgControl.deserialize(data)
            self.messageFunctions[message.type_](message)

# FIXME : Client need to connect to the appropriate server

import socket
import threading
import time
from message_db import Message, MessageController, MessageTypes
from globals_ import  TIMEOUT
import config
from tools.socket_tools import check_ip_port

#import threading
import cgitb 
cgitb.enable(format = 'text')

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
        self.serverName = ""

        self.stopListenFlag = False

        self.clientSocket.settimeout(TIMEOUT) # un-block after 1s

        self.options = ["register", "update", "deregister", "subject", "publish", "ping", "update-server-rq"]

        # message queue
        self.msgQueue = []

        self.runClientFlag = True

        self.isListening = False

    # Message Functions
    def ping_test(self, message):
        self.print_output("PING test succeed with server " + message.text, False)

    def switch_server(self, message):

        # stop listening
        self.stopListenFlag = True

        self.serverName = message.name
        self.serverHost = message.ipAddress
        self.serverPort = message.socketNum

        self.printSignal.PRINT_SERVER_INFO.emit(self.get_server_info()) # update GUI about current server info

        # resume listening
        self.stopListenFlag = False

    def print_registered(self, message):
        self.print_output(self.name + " register acknowledged" )

    def print_updated_socket_info(self, message):
        self.print_output(self.name + "  update network info. acknowledged")
        self.print_output("new ip/port : " + message.ipAddress + " : " + str(message.socketNum))

    def print_registered_denied(self, message):
        self.print_output(self.name + " register denied")
        self.print_output(message.reason)

    def print_updated_socket_info_denied(self, message):
        self.print_output(self.name + " update denied")
        self.print_output(message.reason)

    def print_updated_soi(self, message):
        self.print_output(self.name + " update subject of interests acknowledged")
        self.print_output(str(message.subjects))

    def print_updated_soi_denied(self, message):
        self.print_output(self.name + " update network info. denied")
        self.print_output(message.reason)

    def print_publish_message(self, message):
        self.print_output("News for " + str(message.subjects) + " : " + message.text)

    def print_publish_denied(self, message):
        self.print_output(self.name + " publish news denied")
        self.print_output(message.reason)

    # Class Functions
    def listenMsg(self):
        data, addr = self.clientSocket.recvfrom(1024)
        return data, addr

    def sendMsg(self, msg):
        self.clientSocket.sendto(msg, (self.serverHost, self.serverPort)) # FIXME : needs to be server host, port no ?
    
    def sendBothServer(self, msg):
        # send to both servers
        serverAHost = config.read_data("A", "host")
        serverAPort = config.read_data("A", "port")
        serverBHost = config.read_data("B", "host")
        serverBPort = config.read_data("B", "port")

        self.clientSocket.sendto(msg, (serverAHost, serverAPort)) # FIXME : needs to be server host, port no ?
        self.clientSocket.sendto(msg, (serverBHost, serverBPort)) # FIXME : needs to be server host, port no ?

    def update_host_port(self):
        # FIXME : since timeout 1s, there is a possbility that we are listenMsg + bind at the same time == ERROR
        # stop listening
        self.stopListenFlag = True

        while self.isListening: # wait for socket to stop listening before doing anything else
            time.sleep(TIMEOUT)
            print("socket still listening ...")

        newHost = input("host : ")
        newPort = int(input("port : "))

        # check if valid
        valid = check_ip_port(newHost, newPort)

        if valid:
            # legal

            # set ip/port
            self.HOST = newHost
            self.PORT = newPort

            # NOTE : Need to close and make a new socket before updating new ip address and port
            # close socket
            self.clientSocket.shutdown(socket.SHUT_RD)
            self.clientSocket.close()

            # create new socket
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.clientSocket.bind((self.HOST, self.PORT))
            self.clientSocket.settimeout(TIMEOUT) # un-block after 1s

        # resume listening
        self.stopListenFlag = False

        return valid
    
    def set_server(self, host, port, name):
        self.serverHost = host
        self.serverPort = port
        self.serverName = name

    def get_server_info(self):
        return "server " + self.serverName + " -> " + self.serverHost + " : " + str(self.serverPort)

    def run(self):
        msgThread = threading.Thread(target=self.msg_thread)
        msgThread.start()

        listenThread = threading.Thread(target=self.listen_thread)
        listenThread.start()

        queueThread = threading.Thread(target=self.run_msg_queue)
        queueThread.start()

    def start(self):
        listenThread = threading.Thread(target=self.listen_thread)
        listenThread.start()

        queueThread = threading.Thread(target=self.run_msg_queue)
        queueThread.start()

    def stop(self):
        self.runClientFlag = False

    def connect(self):
        msg = Message(type_ = MessageTypes.CONNECT, name = self.name)
        # self.sendMsg(self.msgControl.serialize(msg))
        self.sendBothServer(self.msgControl.serialize(msg))

    def disconnect(self):
        # # tell the server client to disconnect
        msg = Message(type_ = MessageTypes.DISCONNECT, name = self.name)
        # self.sendMsg(self.msgControl.serialize(msg))

        self.sendBothServer(self.msgControl.serialize(msg))
                
    def listen_thread(self):
        self.runClientFlag = True
        self.isListening = False

        while self.runClientFlag:
            time.sleep(0.001)
            if not self.stopListenFlag:
                try:
                    self.isListening = True
                    
                    data, addr = self.listenMsg()
                    message = self.msgControl.deserialize(data)
                    
                    # add to queue
                    self.msgQueue.append(message)

                except socket.timeout:
                    # print("server time out")
                    self.isListening = False
                    pass

                finally:
                    self.isListening = False

    def run_msg_queue(self):
        while self.runClientFlag:
            time.sleep(0.001)
            if len(self.msgQueue) > 0:
                message = self.msgQueue.pop(0)
                self.messageFunctions[message.type_](message)
            
# GUI related functions

    def init(self):
        # tell the server client is connected
        self.connect()

    def set_print_signal(self, printSignal):
        self.printSignal = printSignal

    def set_output_box(self, outputBox):
        self.outputBox = outputBox

    def print_output(self, text = "default", includeServer = True):
        # print(text)
        if includeServer:
            self.printSignal.PRINT_MSG.emit("server " + self.serverName + " - " + text) # signal emitted to print out in GUI
        else:
            self.printSignal.PRINT_MSG.emit(text) # signal emitted to print out in GUI

    def update_host_port_ui(self, newHost, newPort):
        # FIXME : since timeout 1s, there is a possbility that we are listenMsg + bind at the same time == ERROR

        newPort = int(newPort)

        while self.isListening: # wait for socket to stop listening before doing anything else
            time.sleep(0.1)
            print("socket still listening ...")

        # stop listening
        self.stopListenFlag = True

        valid = check_ip_port(newHost, newPort)

        if valid:
            # legal

            # set ip/port
            self.HOST = newHost
            self.PORT = newPort

            # NOTE : Need to close and make a new socket before updating new ip address and port
            # close socket
            self.clientSocket.shutdown(socket.SHUT_RD)
            self.clientSocket.close()

            # create new socket
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.clientSocket.bind((self.HOST, self.PORT))
            self.clientSocket.settimeout(TIMEOUT) # un-block after 1s

        # resume listening
        self.stopListenFlag = False

        return valid

    def send_message(self, messageType, messageData):
        if messageType == MessageTypes.REGISTER.value:
              
            msg = Message(type_ = MessageTypes.REGISTER, rqNum = 1, name = self.name, 
                ipAddress = self.HOST, socketNum = self.PORT, host = self.HOST, port = self.PORT)

            self.sendBothServer(self.msgControl.serialize(msg))

            # connect the client
            self.connect()

        elif messageType == MessageTypes.UPDATE.value:

            # tell the server to disconnect the client
            self.disconnect()
            
            # update host and port
            valid = self.update_host_port_ui(messageData["ipAddress"], messageData["socketNum"])
            
            if valid:
                msg = Message(type_ = MessageTypes.UPDATE, rqNum = 1, name = self.name, 
                    ipAddress = self.HOST, socketNum = self.PORT, host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

            else:
                self.print_output("invalid ip/port", False)

            # tell the server to connect the client
            self.connect()
            
        elif messageType == MessageTypes.DEREGISTER.value:
            
            msg = Message(type_ = MessageTypes.DEREGISTER, rqNum = 1, name = self.name, host = self.HOST, port = self.PORT)

            self.sendMsg(self.msgControl.serialize(msg))

        elif messageType == MessageTypes.PUBLISH.value:
            subjects = messageData["subjects"]

            if len(subjects) > 1:
                print("too many subjects")

            else:
                news = messageData["text"]
                msg = Message(type_ = MessageTypes.PUBLISH, rqNum = 1, name = self.name, subjects = subjects, text = news,  host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

        elif messageType == MessageTypes.SUBJECTS.value:
                print(["ps", "xbox", "pc", "nintendo", "vr"])
                subjects = messageData["subjects"]
    
                msg = Message(type_ = MessageTypes.SUBJECTS, rqNum = 1, name = self.name, subjects = subjects, host = self.HOST, port = self.PORT)

                self.sendMsg(self.msgControl.serialize(msg))

        elif messageType == MessageTypes.PING.value:
            msg = Message(type_ = MessageTypes.PING, rqNum = 1, name = self.name, host = self.HOST, port = self.PORT)
            self.sendMsg(self.msgControl.serialize(msg))

        elif messageType == MessageTypes.UPDATE_SERVER_REQ.value:
            msg = Message(type_ = MessageTypes.UPDATE_SERVER_REQ, rqNum = 1, name = self.name, host = self.HOST, port = self.PORT, isServer=True)
            self.sendBothServer(self.msgControl.serialize(msg))

        else:
            print("invalid choice")

# NOTE : the reason why the update message (updating the client ip/port) didnt work before was because the socket
# was listening when we close the connection. Therefore, we need to wait for the listening to be over before closing.
# also have to set the timeout again as well
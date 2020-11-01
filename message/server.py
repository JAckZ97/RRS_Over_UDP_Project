#!/usr/bin/env python3

# imports
import socket
# user imports
from message_db import Message, MessageController
from message_db import MessageTypes as mt

# switch functions
def register():
    print("register user")

def update():
    print("update user")

msgFunctions = {
    mt.Register: register,
    mt.Update: update,

}

ipAddress = "127.0.0.1"
portNo = 6789

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind((ipAddress, portNo))

msgControl = MessageController()

while True:
    data, addr = serverSock.recvfrom(1024)
    type_ = msgControl.deserialize(data).type_
    print("message : ", type_)

    # activate function
    msgFunctions[type_]()

#!/usr/bin/env python3

# imports
import socket
# user imports
from message_db import Message, MessageController, MessageTypes

ipAddress = "127.0.0.1"
portNo = 6789
msg = Message(MessageTypes.Update)

msgControl = MessageController()

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSock.sendto(msgControl.serialize(msg), (ipAddress, portNo))

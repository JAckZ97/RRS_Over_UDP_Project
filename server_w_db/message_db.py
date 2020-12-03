#!/usr/bin/env python3
# imports
import pickle
import enum
import random

class MessageTypes(enum.Enum):
    # Subject of interests
    SUBJECTS = "subject"
    SUBJECTS_UPDATED = "subject-updated"
    SUBJECTS_REJECTED = "subject-rejected"

    # Register
    REGISTER = "register"
    REGISTERED = "registered"
    DEREGISTER = "deregister"
    REGISTER_DENIED = "register-denied"
    DEREGISTERED = "deregistered"

    #Update
    UPDATE = "update"
    UPDATE_CONFIRMED = "udpate-confirmed"
    UPDATE_DENIED = "update-denied"

    #Publish
    PUBLISH = "publish"
    MESSAGE = "message"
    PUBLISH_DENIED = "publish-denied"

    #Sever Switching
    CHANGE_SERVER = "change-server"

    # Ping Test
    PING = "ping"

class Message:
    def __init__(self, type_, rqNum = 0, name = "", ipAddress = "", socketNum = 0, reason = "", subjects = None, text = "", host = "", port = 0, isServer = False):

        requestNumber = random.randint(1, 10000)        
        if requestNumber < 0:
            requestNumber *= -1

        # variables
        self.type_ = type_
        self.rqNum = rqNum
        self.name = name
        self.ipAddress = ipAddress
        self.socketNum = socketNum
        self.reason = reason
        self.subjects = subjects
        self.text = text

        self.host = host
        self.port = port

        self.isServer = isServer

class MessageController:
    def __init__(self):
        pass

    def serialize(self, message):
        """
        Arguments
        ---------
        message : Message
            message to be sent
        """
        data = pickle.dumps(message)
        return data

    def deserialize(self, message):
        """
        Arguments
        ---------
        message : Message
            message to be read
        """
        data = pickle.loads(message)
        return data

#!/usr/bin/env python3
# imports
import pickle
import enum
import random

class MessageTypes(enum.Enum):
    Default = "default"
    Register = "register"
    Deregister = "deregister"
    Registered = "registered"
    RegisterDenied = "register-denied"
    Update = "update"

class Message:
    def __init__(self, type_):

        requestNumber = random.randint()        
        if requestNumber < 0:
            requestNumber *= -1

        # variables
        self.type_ = type_
        self.rqNum = requestNumber
        self.name = "Default User"
        self.ipAddress = "localhost"
        self.socketNum = 8888
        self.reason = ""
        self.subjects = []
        self.text = ""

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

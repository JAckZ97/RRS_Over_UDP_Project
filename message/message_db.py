#!/usr/bin/env python3
# imports
import pickle
import enum

class MessageTypes(enum.Enum):
    Default = "default"
    Register = "register"
    Deregister = "deregister"
    RegisterAccept = "register-accept"
    RegisterDeny = "register-deny"
    Update = "update"

class Message:
    def __init__(self, type_):

        # variables
        self.type_ = type_

        self.rqNum = 0
        self.name = "default"
        self.ipAddress = "0.0.0.0"
        self.socketNum = 0
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

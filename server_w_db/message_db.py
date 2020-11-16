#!/usr/bin/env python3
# imports
import pickle
import enum
import random

class MessageTypes(enum.Enum):
    # Default = "default"
    # Register = "register"
    # Deregister = "deregister"
    # Registered = "registered"
    # RegisterDenied = "register-denied"
    # Update = "update"

    # Subject of interests
    SUBJECTS = "subject"
    SUBJECTS_UPDATED = "subject-updated"
    SUBJECTS_REJECTED = "subject-rejected"

    # Register
    REGISTER = "register"

class Message:
    def __init__(self, type_, rqNum = 0, name = "", ipAddress = "", socketNum = 0, reason = "", subjects = None, text = ""):

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

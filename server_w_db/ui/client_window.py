#!/usr/bin/env python3
 # * author : Philippe Vo
 # * date : Aug-22-2020 16:08:02

# * Imports
# 3rd Party Imports
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
# User Imports
from ui.client_widgets import MessageComboBox, InputBox, SendButton, SendStatus, OutputBox

# * Code
class ClientWindow(QtWidgets.QMainWindow):
    """
    client window
    """
    def __init__(self, messageTypes, clientName):
        super(ClientWindow, self).__init__()

        # setup ui
        self.setup_ui(messageTypes)
        # self.setMinimumSize(700, 500)

        self.setWindowTitle(clientName) 

    def setup_ui(self, messageTypes):
        """
        setup the ui
        """
        # Layout
        self.layout = QtWidgets.QGridLayout()

        # Add Widgets
        self.messageCb = MessageComboBox(messageTypes)

        self.sendButton = SendButton()
        self.inputWindow = InputBox(self.sendButton.messageData)
        self.sendStatus = SendStatus()
        self.msgWindow = OutputBox()

        # Add Widgets Functionality
        self.messageCb.currentIndexChanged.connect(self.choose_message_type)
        self.messageCb.setCurrentIndex(0) # set to register

        # Add layouts
        self.layout.addWidget(self.messageCb, 0, 0)
        self.layout.addWidget(self.inputWindow, 1, 0)
        self.layout.addWidget(self.sendButton, 2, 0)
        self.layout.addWidget(self.sendStatus, 2, 1)
        self.layout.addWidget(self.msgWindow, 1, 1)

        # Apply Layout
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.layout)

    def choose_message_type(self):
        self.sendButton.set_msg_type(self.messageCb.currentText())
#!/usr/bin/env python3
 # * author : Philippe Vo
 # * date : Aug-22-2020 16:08:02

# * Imports
# 3rd Party Imports
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
# User Imports
from ui.client_widgets import MessageComboBox, InputBox, SendButton, SendStatus, OutputBox, PrintSignal, ServerInfo

# * Code
class ClientWindow(QtWidgets.QMainWindow):
    """
    client window
    """
    def __init__(self, messageTypes, clientName, serverInfo):
        super(ClientWindow, self).__init__()

        # setup ui
        self.setup_ui(messageTypes, serverInfo)
        # self.setMinimumSize(700, 500)

        self.setWindowTitle(clientName) 

    def setup_ui(self, messageTypes, serverInfo):
        """
        setup the ui
        """
        # Layout
        self.layout = QtWidgets.QGridLayout()

        # Add Widgets
        self.messageCb = MessageComboBox(messageTypes)

        self.sendButton = SendButton()
        self.inputWindow = InputBox(self.sendButton.messageData)
        self.msgWindow = OutputBox()
        self.serverInfo = ServerInfo(serverInfo)

        self.printSignal = PrintSignal()
        self.printSignal.PRINT_MSG.connect(self.msgWindow.print_2_window)
        self.printSignal.PRINT_SERVER_INFO.connect(self.serverInfo.set_server_info)

        # Add Widgets Functionality
        self.messageCb.currentIndexChanged.connect(self.choose_message_type)
        self.messageCb.setCurrentIndex(0) # set to register

        # Add layouts
        self.layout.addWidget(self.messageCb, 0, 0)
        self.layout.addWidget(self.serverInfo, 0, 1)
        self.layout.addWidget(self.inputWindow, 1, 0)
        self.layout.addWidget(self.sendButton, 2, 0)
        self.layout.addWidget(self.msgWindow, 1, 1)

        # Apply Layout
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.layout)

    def choose_message_type(self):
        self.sendButton.set_msg_type(self.messageCb.currentText())

    def bark(self):
        pass
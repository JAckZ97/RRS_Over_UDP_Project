#!/usr/bin/env python3
 # * author : Philippe Vo
 # * date : Aug-22-2020 16:08:02

# * Imports
# 3rd Party Imports
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, Slot                            

# SIZES
INPUT_BOX_MIN_SIZE = [200,300]
OUTPUT_BOX_MIN_SIZE = [200,300]
LABEL_MIN_SIZE = [50,10]
INPUT_MIN_SIZE = [50,10]

class MessageComboBox(QtWidgets.QComboBox):
    def __init__(self, messageTypes):
        super(MessageComboBox, self).__init__()

        self.addItems(messageTypes)
        self.setCurrentIndex(-1) # so that we can set the default message command to register

class InputBox(QtWidgets.QGroupBox):
    def __init__(self, messageData):
        super(InputBox, self).__init__()

        # Init.
        self.setMinimumSize(INPUT_BOX_MIN_SIZE[0], INPUT_BOX_MIN_SIZE[1])

        # Layout
        self.layout = QtWidgets.QVBoxLayout()

        # Add Widgets
        self.ipAddress = InputLine("ipAddress", messageData)
        self.socketNum = InputLine("socketNum", messageData)
        self.reason = InputLine("reason", messageData)
        self.subjects = InputLine("subjects", messageData)
        self.text = InputLine("text", messageData)

        #To allow only int
        self.onlyInt = QtGui.QIntValidator()
        self.socketNum.line.setValidator(self.onlyInt)

        self.layout.addWidget(self.ipAddress)
        self.layout.addWidget(self.socketNum)
        self.layout.addWidget(self.reason)
        self.layout.addWidget(self.subjects)
        self.layout.addWidget(self.text)

        # Apply Layout
        self.setLayout(self.layout)

    def clear(self):
        pass

class InputLine(QtWidgets.QWidget):
    def __init__(self, name, messageData):
        super(InputLine, self).__init__()

        # Init.
        self.messageData = messageData

        # Layout
        self.layout = QtWidgets.QHBoxLayout()

        # Add Widgets
        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel(name)

        self.line.setMinimumSize(INPUT_MIN_SIZE[0],INPUT_MIN_SIZE[1])
        self.label.setMinimumSize(LABEL_MIN_SIZE[0],LABEL_MIN_SIZE[1])

        self.line.textChanged.connect(self.set_data)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)

        # Apply Layout
        self.setLayout(self.layout)

    def set_data(self):
        # if it is subjects, then split it
        if self.label.text() == "subjects":
            subjects = self.line.text().split()

            self.messageData[self.label.text()] = subjects

        else:
            self.messageData[self.label.text()] = self.line.text()

class SendButton(QtWidgets.QPushButton):
    def __init__(self):
        super(SendButton, self).__init__()

        # Init.
        self.setText("Send")
        self.messageType = "default"
        self.messageData = {
            "ipAddress": "default",
            "socketNum": 0,
            "reason": "default",
            "subjects": "default",
            "text": "default"
        }

    def set_msg_type(self, messageType):
        self.messageType = messageType

    def set_msg_data(self, messageData):
        self.messageData = messageData
    
    def set_func(self, sendFunc):
        self.sendFunc = sendFunc

        # Function run
        self.clicked.connect(lambda: self.sendFunc(self.messageType, self.messageData))

class SendStatus(QtWidgets.QLabel):
    def __init__(self):
        super(SendStatus, self).__init__()

        # Init.
        self.setText("send status")

    def accepted(self):
        self.setText("sent")

    def rejected(self):
        self.setText("sent failed")

class PrintSignal(QtCore.QObject):
    PRINT = QtCore.Signal(str)

    def __init__(self):
        super(PrintSignal, self).__init__()

    #     self.PRINT.connect(self.print_output)

    #     self.outputBox = outputBox

    # def print_output(self):
    #     self.outputBox.print_2_window()

class OutputBox(QtWidgets.QPlainTextEdit):
    
    def __init__(self):
        super(OutputBox, self).__init__()

        # Init.
        self.setMinimumSize(OUTPUT_BOX_MIN_SIZE[0], OUTPUT_BOX_MIN_SIZE[1])

        # Init.
        self.setPlaceholderText("msg output box")
        self.setReadOnly(True)

    @Slot(str)
    def print_2_window(self, text):
        self.appendPlainText(text)


class SubjectsType(QtWidgets.QLabel):
    def __init__(self):
        super(SubjectsType, self).__init__()

        # Init.
        self.setText("List of subjects: [pc, xbox, pc, nintendo, vr]")

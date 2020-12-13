# * Imports
# 3rd Party Imports
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
# User Imports
from ui.client_window import ClientWindow
from Client_class import Client
from globals_ import serverAHost, serverAPort, serverBHost, serverBPort

"""
TODO - for some reason, tryin to register 4th is not working
TODO - register as deafult message command
TODO - updating ipadress of client -> and then restart the system (get error since ipaddress in test_client is not the same)
TODO - show the available subjects
TODO - random crashes (when you spam message commands) -> maybe because of the timeout
TODO - for some reason the UPDATE message is not working ...
TODO - put all the message commands
TODO - blur inputline that not from message commands
TODO - connect client at the beggining if we remove the client.run()
TODO - make window nicer (send msg icon, color scheme, font)
"""
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def setup_client():
    client = Client("HAOCHENG", "127.0.0.10", 8888)
    client.set_server(serverAHost, serverAPort)

    return client

def setup_window(client):
    # Open MainWindow
    clientWindow = ClientWindow(client.options, client.name)

    # set send button function
    clientWindow.sendButton.set_func(client.send_message)

    # set output box
    client.set_output_box(clientWindow.msgWindow)

    return clientWindow

def close(app, clients):
    app.exec_()
    
    # close and disconnect clients 
    for client in clients:
        client.disconnect()
        client.stop()

    print("done")

# * Code
if __name__ == '__main__':

    sys.excepthook = except_hook

    # Init App
    app = QtWidgets.QApplication(sys.argv)

    # load font
    # fontDb = QtGui.QFontDatabase()
    # fontPixel = fontDb.addApplicationFont("resources/fonts/dogicapixel.ttf")

    # load stylesheet
    # with open("resources/style.qss", "r") as f:
    #     app.setStyleSheet(f.read())

    # Input Clients
    # clients = []
    # for i in range(2):
    #     print("Information format: Name IP Port")
    #     data = input("Enter client information: ")
    #     messageList = data.split()

    #     if len(messageList) != 3:
    #         print("must enter proper format")
    #         sys.exit()

    #     client = Client(messageList[0], messageList[1], int(messageList[2]))
    #     clients.append(client)

    
    clientA = Client("HAOCHENG", "127.0.0.10", 8888)
    clientA.set_server(serverAHost, serverAPort)
    clientB = Client("JACK", "127.0.0.11", 8888)
    clientB.set_server(serverAHost, serverAPort)
    clientC = Client("PHIL", "127.0.0.12", 8888)
    clientC.set_server(serverAHost, serverAPort)
    clientD = Client("BOB", "127.0.0.13", 8888)
    clientD.set_server(serverAHost, serverAPort)
    
    clients = [clientA, clientB, clientC, clientD]

    # windowA = setup_window(clientA)
    # # Start Client Thread
    # clientA.start()
    # # Show Window
    # windowA.show()

    # windowB = setup_window(clientB)
    # # Start Client Thread
    # clientB.start()
    # # Show Window
    # windowB.show()
    try:
        # Open Window
        windows = []
        for client in clients:
            window = setup_window(client)

            # Show Window
            windows.append(window)

        for client in clients:
            # Start Client Thread
            client.start()

        for window in windows:
            window.show()

        # Exit
        sys.exit(close(app, clients))

    except Exception as e:
        print(e)
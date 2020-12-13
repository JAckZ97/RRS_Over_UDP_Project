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
TODO - updating ipadress of client -> and then restart the system (get error since ipaddress in test_client is not the same)
TODO - show the available subjects
TODO - random crashes (when you spam message commands) -> maybe because of the timeout
TODO - for some reason the UPDATE message is not working ...
TODO - put all the message commands
TODO - blur inputline that not from message commands
TODO - connect client at the beggining if we remove the client.run()
TODO - make window nicer (send msg icon, color scheme, font)
"""

def setup_client():
    client = Client("HAOCHENG", "127.0.0.10", 8888)
    client.set_server(serverAHost, serverAPort)

    return client

def setup_window(client):
    # Open MainWindow
    clientWindow = ClientWindow(client.options)

    # set send button function
    clientWindow.sendButton.set_func(client.send_message)

    # set output box
    client.set_output_box(clientWindow.msgWindow)

    return clientWindow

# * Code
if __name__ == '__main__':

    # Init App
    app = QtWidgets.QApplication(sys.argv)

    # load font
    # fontDb = QtGui.QFontDatabase()
    # fontPixel = fontDb.addApplicationFont("resources/fonts/dogicapixel.ttf")

    # load stylesheet
    # with open("resources/style.qss", "r") as f:
    #     app.setStyleSheet(f.read())

    # Setup Client
    clientA = Client("HAOCHENG", "127.0.0.10", 8888)
    clientA.set_server(serverAHost, serverAPort)

    clientB = Client("JACK", "127.0.0.11", 8888)
    clientB.set_server(serverAHost, serverAPort)

    # Open Window
    windowA = setup_window(clientA)
    windowB = setup_window(clientB)

    # Start Client Thread
    clientA.run()
    clientB.run()

    # Show Window
    windowA.show()
    windowB.show()

    try:
        # Exit
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        client.stop()
        print("done.")
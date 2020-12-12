# * Imports
# 3rd Party Imports
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
# User Imports
from ui.client_window import ClientWindow

"""
TODO - for some reason the UPDATE message is not working ...
TODO - put all the message commands
TODO - blur inputline that not from message commands
TODO - connect client at the beggining if we remove the client.run()
TODO - make window nicer (send msg icon, color scheme, font)
"""

def thread_function(name):
    import time
    for i in range(10):
        print(i)
        time.sleep(2)

def setup_client():
    from Client_class import Client
    from globals_ import serverAHost, serverAPort, serverBHost, serverBPort
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

    # Setup CLient
    client = setup_client()

    # Open Window
    window = setup_window(client)

    # Start Client Thread
    client.run()

    # Show Window
    window.show()

    # Exit
    sys.exit(app.exec_())
# * Imports
# 3rd Party Imports
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
# User Imports
from ui.client_window import ClientWindow
from ui.client_widgets import PrintSignal
from client import Client
import config
from tools.socket_tools import check_ip_port

"""
- important
TODO - prepare report + diagrams (to explain our program and system)
TODO - install program on laptop for demo (philippe)
TODO - switch every x minutes !

- less important
TODO - rqNum add
TODO - improve the print messages that are sent from server to client, vice versa
TODO - change run_msg_queue -> process_thread (naming)
TODO - show client ip/port on GUI

- luxury
TODO - make window nicer (send msg icon, color scheme, font)
TODO - cleanup code - filenames

- done
TODO - connect client at the beggining if we remove the client.run()
TODO - server update ip/port
TODO - sometimes trying to update server ip/port -> stuck in socket listening while loop
TODO - adding user information
TODO - show the available subjects
TODO - have a list of ip/port being used
TODO - blur inputline that not from message commands
TODO - README -> write the non-optimized stuff
        - no ability to check if server is still up or not (client perspective)
        TODO - show which server is running on the client side

- not done
TODO - shutdown server handling on the client side

"""
def ReadQss(style):
    with open(style, 'r') as f:
        return f.read()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def setup_window(client):
    # Open MainWindow
    serverInfo = client.get_server_info()
    userNetworkInfo = client.get_user_network_info()
    clientWindow = ClientWindow(client.options, client.name, serverInfo, userNetworkInfo)

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
    fontDb = QtGui.QFontDatabase()
    fontPixel = fontDb.addApplicationFont("ui/resources/fonts/dogicapixel.ttf")

    # load stylesheet
    with open("ui/resources/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Input Clients
    # clients = []
    # for i in range(2):
    #     print("Information format: Name IP Port")
    #     data = input("Enter client information: ")
    #     messageList = data.split()

    #     if len(messageList) != 3:
    #         print("must enter proper format")
    #         sys.exit()
        
    #     name = messageList[0]
    #     host = messageList[1]
    #     port = int(messageList[2])

    #     valid = check_ip_port(host, port)

    #     if valid:
    #         client = Client(name, host, port)
    #         clients.append(client)

    #     else:
    #         print("invalid ip/port")
    #         sys.exit()

    serverAHost = config.read_data("A", "host")
    serverAPort = config.read_data("A", "port")
    
    clientA = Client("HAOCHENG", "127.0.0.10", 8888)
    clientA.set_server(serverAHost, serverAPort, "A")
    clientB = Client("JACK", "127.0.0.11", 8888)
    clientB.set_server(serverAHost, serverAPort, "A")
    clientC = Client("PHIL", "127.0.0.12", 8888)
    clientC.set_server(serverAHost, serverAPort, "A")
    clientD = Client("BOB", "127.0.0.13", 8888)
    clientD.set_server(serverAHost, serverAPort, "A")
    
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

    # Open Window
    windows = []
    for client in clients:
        window = setup_window(client)

        # set signal
        client.set_print_signal(window.printSignal) 
        # NOTE : if we dont add this, it causes random crashes since we trying to update the GUI from another thread ... 

        # Show Window
        windows.append(window)

    for client in clients:
        # Start Client Thread
        client.start()

    for window in windows:

        styleFile = './ui/Style.qss'
        qssStyle = ReadQss(styleFile)
        window.setStyleSheet(qssStyle)

        window.show()

    # Exit
    sys.exit(close(app, clients))


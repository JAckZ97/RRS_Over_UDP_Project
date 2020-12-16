from client import Client
import config

"""
server info
serverA = Server("A", "127.0.0.1", 8888)
serverB = Server("B", "127.0.0.2", 8887)
"""

data = int(input("client (0,1,2) : "))

serverAHost = config.read_data("A", "host")
serverAPort = config.read_data("A", "port")

if data == 0:
    client = Client("HAOCHENG", "127.0.0.10", 8888)
    client.set_server(serverAHost, serverAPort)
    client.run()
elif data == 1:
    client = Client("JACK", "127.0.0.11", 8888)
    client.set_server(serverAHost, serverAPort)
    client.run()
elif data == 2:
    client = Client("PHIL", "127.0.0.12", 8888)
    client.set_server(serverAHost, serverAPort)
    client.run()
else:
    print("invalid choice")

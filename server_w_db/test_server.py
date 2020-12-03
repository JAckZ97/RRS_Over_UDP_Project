from Server_class import Server
from globals_ import serverAHost, serverAPort, serverBHost, serverBPort
from globals_ import databaseAFilePath, databaseBFilePath

import time
import random

# methods
def switch_server(closeServer, runServer):
    # closeServer : Server to be closed
    # runServer : server to replace closed server

    # run new server
    runServer.start()
    
    # message clients that server will close and they need to switch
    # FIXME : Needs further testing ...
    closeServer.server_switch_msg(runServer)

    # close old server
    closeServer.pause()

    # pass

# globals
exitFlag = False

# init servers and clients
serverA = Server("A", serverAHost, serverAPort, databaseAFilePath)
serverB = Server("B", serverBHost, serverBPort, databaseBFilePath)

# letting server know each other
serverA.set_otherServer(serverB)
serverB.set_otherServer(serverA)

# serverA.run()

# # run system
while not exitFlag:
    # switch listening server every random minutes

    # NOTE : Server A starts first

    switch_server(serverA,serverB)

    time.sleep(random.randint(1,3))

    switch_server(serverB,serverA)

    time.sleep(random.randint(1,3))

from Server_class import Server
from globals_ import serverAHost, serverAPort, serverBHost, serverBPort

import time
import random

# methods
def switch_server(closeServer, runServer):
    # closeServer : Server to be closed
    # runServer : server to replace closed server

    # run new server
    runServer.start()
    
    # message clients that server will close and they need to switch
    # FIXME : NEED TO IMPLEMENT !!!!

    # close old server
    closeServer.pause()

    # pass

# globals
exitFlag = False

# init servers and clients
serverA = Server("A", serverAHost, serverAPort)
serverB = Server("B", serverBHost, serverBPort)

# serverA.run()

# # run system
while not exitFlag:
    # switch listening server every random minutes

    # time.sleep(random.randint(1,60))
    time.sleep(3)

    switch_server(serverA,serverB)

    # time.sleep(random.randint(1,60))
    time.sleep(4)

    switch_server(serverB,serverA)

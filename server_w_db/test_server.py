from Server_class import Server

import time
import random

# methods
def switch_server(closeServer, runServer):
    # closeServer : Server to be closed
    # runServer : server to replace closed server

    # run new server
    runServer.start()
    
    # message clients that server will close and they need to switch

    # close old server
    closeServer.pause()

    # pass

# globals
exitFlag = False

# init servers and clients
serverA = Server("A", "127.0.0.1", 8888)
serverB = Server("B", "127.0.0.2", 8887)

serverA.run()

# # run system
# while not exitFlag:
#     # switch listening server every random minutes
  
#     # time.sleep(random.randint(1,60))
#     time.sleep(3)

#     switch_server(serverA,serverB)

#     # time.sleep(random.randint(1,60))
#     time.sleep(4)

#     switch_server(serverB,serverA)
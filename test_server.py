from server import Server
import config

import time
import random
import threading

# methods
def switch_server(closeServer, runServer):
    # closeServer : Server to be closed
    # runServer : server to replace closed server

    # run new server
    runServer.resume()

    # message clients that server will close and they need to switch
    # FIXME : Needs further testing ...
    closeServer.server_switch_msg(runServer)

    # close old server
    closeServer.pause()

    # pass

# globals
exitFlag = False

# read config
databaseAFilePath = config.read_data("A", "databaseFile")
databaseBFilePath = config.read_data("B", "databaseFile")
serverAHost = config.read_data("A", "host")
serverAPort = config.read_data("A", "port")
serverBHost = config.read_data("B", "host")
serverBPort = config.read_data("B", "port")

# init servers and clients
serverA = Server("A", serverAHost, serverAPort, databaseAFilePath)
serverB = Server("B", serverBHost, serverBPort, databaseBFilePath)

# letting server know each other
serverA.set_otherServer(serverB)
serverB.set_otherServer(serverA)

serverA.start()
serverB.start()
# serverB.pause()

minMinute = 1
maxMinute = 5

switchTimeMin = minMinute * 60
switchTimeMax = maxMinute * 60

try:
    # # run system
    while not exitFlag:
        # switch listening server every random minutes

        # NOTE : Server A starts first

        # if serverA.clients_online() >= 1: # only switch if there is at leats one client online

        switch_server(serverA,serverB)

        time.sleep(random.randint(switchTimeMin,switchTimeMax))

        switch_server(serverB,serverA)

        time.sleep(random.randint(switchTimeMin,switchTimeMax))

except KeyboardInterrupt:
    serverA.stop()
    serverB.stop()
    print("done.")

# FIXME 
# currently, the only "hiccup" is that when we update the ipaddress + port of the
# user, we need to manuall;y change it in the test_client
# again since or else there will be mistmatch with the database one

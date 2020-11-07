import socket
import sys
import yaml
from message_db import Message, MessageController
from message_db import MessageTypes as mt
from database import DatabaseController 

HOST = 'localhost' 
PORT = 8888 


''' data model
User :
    Client_Name : 
    IP_address : 
    Socket_Number :
    Register_Status :
    Subject_of_Interest :
'''

# create socket
try :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print ('Socket created')
except socket.error as msg :
    print ('Failed to create socket.' + ' Message ' + msg[1])
    sys.exit()


# bind socket 
try:
    sock.bind((HOST, PORT))
    print ('Socket bind complete')
except socket.error as msg:
    print ('Bind failed. ' + ' Message ' + msg[1])
    sys.exit()


msgControl = MessageController()
database = DatabaseController()

while True:

    try:
        data, addr = sock.recvfrom(1024)

        if not data: 
            break

        '''
        if database.checkExistUser() == True:
            reply = (b'REGISTER-DENIED ')
        else:
            # reply message
            reply = (b'REGISTERED ')

        name = msgControl.deserialize(data).name
        '''

        # load reply message into yaml
        database.updateFile(msgControl.deserialize(data))

        # read from yaml
        # sock.sendto(database.readFile() , addr)

        # break


    # use ctrl + break to terminate
    except KeyboardInterrupt:
        print ('Interrupted')
        sys.exit(0)

sock.close()



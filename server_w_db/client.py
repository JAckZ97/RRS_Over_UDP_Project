import socket
import sys
from message_db import Message, MessageController, MessageTypes

HOST = 'localhost' 
PORT = 8888 

try :
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print ('Failed to create socket: '+ msg[1])
    sys.exit()


while True :
    # msg = b'hello server. '
    msg = Message(MessageTypes.Register)

    try :
        msgControl = MessageController()
        
        client_sock.sendto(msgControl.serialize(msg), (HOST, PORT))
         
        # data, addr = client_sock.recvfrom(1024)
        # print (data.decode('utf-8'))

        break
     
    except socket.error as msg:
        print (' Message error: ' + msg[1])

client_sock.close()



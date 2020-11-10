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

    try :
        registerMessage = input("Enter message: ")
        messageList = registerMessage.split()

        if messageList[0] == MessageTypes.Register.value:

            msgList = {
                    'Client_Name': messageList[1], 
                    'IP_address': messageList[2], 
                    'Socket_Number': int(messageList[3]), 
                    'Register_Status': True,
                    'Subject_of_Interest': []
                }

            msgControl = MessageController()
            client_sock.sendto(msgControl.serialize(msgList), (HOST, PORT))
            # print('success')
        else:
            print('register not success')

        break
     
    except socket.error as msg:
        print (' Message error: ' + msg[1])

client_sock.close()



import socket
import sys

HOST = 'localhost' 
PORT = 8888 

try :
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg :
    print ('Failed to create socket')
    sys.exit()


while True :
    msg = b'hello server. '

    try :
        client_sock.sendto(msg, (HOST, PORT))
         
        data, addr = client_sock.recvfrom(1024)
         
        print (data.decode('utf-8'))

        break
     
    except socket.error as msg:
        print (' Message ' + msg[1])

client_sock.close()



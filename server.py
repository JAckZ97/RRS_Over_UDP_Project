import socket
import sys

HOST = 'localhost' 
PORT = 8888 

# create socket
try :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print ('Socket created')
except socket.error as msg :
    print ('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()


# bind socket
try:
    sock.bind((HOST, PORT))
    print ('Socket bind complete')
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()


while True:
    # 1024 refer to 1024 bytes
    data, addr = sock.recvfrom(1024)

    if not data: 
        break
    
    reply = (data + b' received.')
    
    # send the message to the client
    sock.sendto(reply , addr)
    print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.decode('utf-8')) 

    break
     
sock.close()



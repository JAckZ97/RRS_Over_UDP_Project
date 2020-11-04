import socket
import sys
import yaml

HOST = 'localhost' 
PORT = 8888 

# TODO:
# handle the message 

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
    # print ('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()


# bind socket
try:
    sock.bind((HOST, PORT))
    print ('Socket bind complete')
except socket.error as msg:
    # print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()


while True:
    # 1024 refer to 1024 bytes
    data, addr = sock.recvfrom(1024)

    if not data: 
        break
    
    # reply message
    reply = (data + b' received.')

    # load reply message into yaml
    users = {'message': [reply.decode('utf-8')]}
    with open("user_message.yaml", "w") as f:
        data = yaml.dump(users, f)

    # read from yaml
    with open("user_message.yaml") as f:
        docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in docs:
            for k, v in doc.items():
                # print(k, "->", v)

                # send the message to the client
                sock.sendto(" ".join(v).encode() , addr)
    
    # print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data) 

    break
     
sock.close()



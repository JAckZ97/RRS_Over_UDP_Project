import socket
import sys
import os

def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    try:
        s.connect((address, port))
        return True
    except socket.error as e:
        return False
    finally:
        s.close()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)

    print("data -> ", data)
    
    if data:
        HOST_UP  = check_server(address[0], address[1])
        if HOST_UP:
            print("host is open")
            sent = sock.sendto("wow".encode(), address)
        else:
            print("host not open")

        
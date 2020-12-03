import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

message = 'This is the message.  It will be repeated.'

try:
    # Send data
    sent = sock.sendto(message.encode(), server_address)

    # Receive response
    data, server = sock.recvfrom(4096)
    print(data)

finally:
    print("close")
    sock.close()
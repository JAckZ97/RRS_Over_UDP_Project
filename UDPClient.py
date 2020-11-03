import socket
import sys

try:
	client_socket=sock.socket(socket.AF_INET.socket.SOCK_DGRAM)
except socket.error as msg:
	print('Failed to create socket')
	sys.exit()



client_socket.sendto[msg.encode("utf-8"),('localhost',8888)]

while True:
	msg="Hello UDP Server, this is the client"
	try:
		client_socket.sendto[msg.encode("utf-8"),('localhost',8888)]

		data.addr=client_socket.recvfrom(1024)

		print(str(data))

	except socket.error as msg:
	print('Error:' + msg)

	client_socket.close()


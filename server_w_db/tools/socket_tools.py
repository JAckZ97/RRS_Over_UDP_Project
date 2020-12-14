import socket

def check_ip_port(ipAddress, portNum):
    try:
        # check if ip is legal
        socket.inet_aton(ipAddress)

        # check if port is legal
        # port should be an integer from 1-65535
        if not(1025 < portNum < 65535):
            raise socket.error

        return True

    except socket.error:
        # Not legal
        print("ip address/port invalid")

        return False
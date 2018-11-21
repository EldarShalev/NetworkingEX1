import sys
from socket import socket, AF_INET, SOCK_DGRAM

def run_client(server_ip, server_port):
	# Open socket
    s = socket(AF_INET, SOCK_DGRAM)
	
	# Get user input
    msg = raw_input("Message to send: ")

    while not msg == 'quit':
		# Send to server
        s.sendto(msg, (server_ip,server_port))
        data, sender_info = s.recvfrom(2048)
		# Print data from server
        print("Server sent: ", data)
        msg = raw_input("Message to send: ")

    s.close()

if len(sys.argv) == 3:
    run_client(sys.argv[1], int(sys.argv[2]))
else:
    print("Bad number of inputs, expected 2(<server-ip><server-port>).")
import sys
from socket import socket, AF_INET, SOCK_DGRAM


def run_server(my_port, parent_ip, parent_port, addresses_file_name):
    with open(addresses_file_name, "r") as f:
        lines = f.read().split("\n")

	# Load to dictionary
    website_ips = {}
    for line in lines:
        address, ip = line.strip().split(',')
        website_ips[address] = ip

	# Open socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('0.0.0.0', my_port))

	# Set parent info
    if parent_ip == "-1" or parent_port == -1:
        parent_info = None
    else:
        parent_info = (parent_ip, parent_port)

	# Listen to requests
    while True:
        data, sender_info = s.recvfrom(2048)
        print("Message: ", data, " from: ", sender_info)
        if data.decode('utf-8') in website_ips:
			# If found in the dictionary
            s.sendto(website_ips[data.decode('utf-8')].encode('utf-8'), sender_info)
        elif parent_info is None:
			# If parent
            s.sendto('Unknown', sender_info)
        else:
			# Ask parent
            s.sendto(data, parent_info)
            address_ip, parent_info = s.recvfrom(2048)

            if address_ip.decode('utf-8') != 'Unknown':
                # Send ip to client
                s.sendto(address_ip, sender_info)
                # Update ips file
                website_ips[data.decode("utf-8")] = address_ip.decode('utf-8')
				text = ''
                for key in website_ips.keys():
                    text += "%s,%s\n" % (key, website_ips[key])
                with open("./ips.txt", "w+") as f:
                    f.write(text[:-1])
            else:
				# Parent returned unknown
                s.sendto(address_ip, sender_info)

if (len(sys.argv) == 5):
    run_server(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4])
else:
    print("Invalid number of arguments")

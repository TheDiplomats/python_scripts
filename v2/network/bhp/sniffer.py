import sys
import socket
import os


def run(host):
	#Note promiscuous mode requires admin/root privileges
	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP
	
	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

	sniffer.bind((host, 0))

	#include IP headers of capture
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	#Windows needs to send an IOCTL for promiscuous mode
	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	
	print(sniffer.recvfrom(65565))

	#Shutdown promiscuous mode on windows
	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
	
	
def main():
	if len(sys.argv[1:]) != 1:
		print('Usage: sniffer.py [host]')
		print('Example: ./proxy.py 192.168.0.196')
		sys.exit(0)
	host = sys.argv[1]
	run(host)

if __name__ == '__main__':
	main()

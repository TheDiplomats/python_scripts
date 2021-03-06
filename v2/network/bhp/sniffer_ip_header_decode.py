import socket
import struct
import os
import sys
from ctypes import *


class IP(Structure):
	_fields_ = [
		('ihl', c_ubyte, 4),
		('version', c_ubyte, 4),
		('tos', c_ubyte),
		('len', c_ushort),
		('id', c_ushort),
		('offset', c_ushort),
		('ttl', c_ubyte),
		('protocol_num', c_ubyte),
		('sum', c_ushort),
		('src', c_ulong),
		('dst', c_ulong)
	]
	
	def __new__(self, socket_buffer=None):
		return self.from_buffer_copy(socket_buffer)
	
	def __init__(self, socket_buffer=None):
		
		# map protocol constants to their names
		self.protocol_map = {1:'ICMP', 6:'TCP', 17:'UDP'}
		
		# readable ip address
		self.src_address = socket.inet_ntoa(struct.pack('<L', self.src))
		self.dst_address = socket.inet_ntoa(struct.pack('<L', self.dst))
		
		# readable protocol
		try:
			self.protocol = self.protocol_map[self.protocol_num]
		except:
			self.protocol = str(self.protocol_num)
			

def run(host):

	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP
	
	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

	sniffer.bind((host, 0))

	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	
	print(sniffer.recvfrom(65565))

	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
	
	try:
		while True:
			# Read packet
			raw_buffer = sniffer.recvfrom(65565)[0]
			# Create IP header from first 20 bytes of the buffer
			ip_header = IP(raw_buffer[0:20])
			# Print protocol & host
			print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
	
	except KeyboardInterrupt:
		if os.name == 'nt':
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
		exit(0)


def main():
	if len(sys.argv[1:]) != 1:
		print('Usage: sniffer_ip_header_decode.py [host]')
		print('Example: sniffer_ip_header_decode.py 192.168.0.196')
		sys.exit(0)
	host = sys.argv[1]
	run(host)

if __name__ == '__main__':
	main()

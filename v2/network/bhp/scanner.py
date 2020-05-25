import time
import threading
import socket
import struct
import os
import sys
from netaddr import IPNetwork, IPAddress
from ctypes import *


class ICMP(Structure):
	_fields_ = [
		('type', c_ubyte),
		('code', c_ubyte),
		('checksum', c_ushort),
		('unused', c_ushort),
		('next_hop_mtu', c_ushort)
	]
	
	def __new__(self, socket_buffer):
		return self.from_buffer_copy(socket_buffer)
	
	def __init__(self, socket_buffer):
		pass


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


# Spray UDP datagrams
def udp_sender(subnet, magic_message):
	time.sleep(5)
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for ip in IPNetwork(subnet):
		try:
			sender.sendto(magic_message, ('%s' % ip, 65212))
		except:
			pass


def run(host, subnet, magic_message):

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
	
	# Start sending packets
	t = threading.Thread(target=udp_sender, args=(subnet, magic_message))
	t.start()
	
	try:
		while True:
			# Read packet
			raw_buffer = sniffer.recvfrom(65565)[0]
			# Create IP header from first 20 bytes of the buffer
			ip_header = IP(raw_buffer[0:20])
			# Print protocol & host
			print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address
			
			if ip_header.protocol == 'ICMP':
				# Calculate where ICMP packet starts
				offset = ip_header.ihl * 4
				buf = raw_buffer[offset:offset + sizeof(ICMP)]
				icmp_header = ICMP(buf)
				print('ICMP -> Type: %d Code: %d' % (icmp_header.type, icmp_header.code))
				if icmp_header.code == 3 and icmp_header.type == 3:
					if IPAddress(ip_header.src_address) in IPNetwork(subnet):
						if raw_buffer[len(raw_buffer) - len(magic_message):] == magic_message:
							print('Host Up: %s' % ip_header.src_address)
	
	except KeyboardInterrupt:
		if os.name == 'nt':
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
		exit(0)


def main():
	if len(sys.argv[1:]) != 3:
		print('Usage: sniffer_ip_header_decode.py [host] [subnet] [magic_message]')
		print('Example: sniffer_ip_header_decode.py 192.168.0.196')
		sys.exit(0)
	host = sys.argv[1]
	subnet = sys.argv[2]
	magic_message = sys.argv[3]
	run(host, subnet, magic_message)

if __name__ == '__main__':
	main()

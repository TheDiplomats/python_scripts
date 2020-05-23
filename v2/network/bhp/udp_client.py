from socket import *
from threading import *
import optparse


screenlock = Semaphore(value=1)


def initialize(host, ports, data):
	try:
		tgtIP = gethostbyname(host)
	except:
		print('[!] Cannot resolve "%s": Unknown host' % host)
		return
	try:
		tgtName = gethostbyaddr(tgtIP)
		print('\n[*] Attempting to connect to : ' + tgtName[0])
	except:
		print('\n[*] Attempting to connect to : ' + tgtIP)
	setdefaulttimeout(3)
	for port in ports:
		t = Thread(target=connect, args=(host, int(port), bytes(data)))
		t.start()
	


def connect(host, port, data):
	setup = ''
	#setup = 'POST / HTTP/1.1\r\nHost: google.com\r\n\r\n'
	payload = bytes(setup + data)
	try:
		client = socket(AF_INET, SOCK_DGRAM)
		client.sendto(payload, (host, port))
		response, addr = client.recvfrom(4096)
		screenlock.acquire()
		print('[*] Sending payload: ' + data)
		print('[*] udp/port %d open:' % port)
		print(str(response))
		
	except:
		screenlock.acquire()
		print('[*] udp/port %d closed' % port)
	finally:
		screenlock.release()
		client.close()
	
	
def main():
	parser = optparse.OptionParser('usage: udp_client.py '+\
		'-H <target host> -p <target port> -d <data payload>')
	parser.add_option('-H', dest='tgtHost', type='string', \
		help='Specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', \
		help='Specify target port(s) seperated by comma, no spaces')
	parser.add_option('-d', dest='tgtData', type='string', \
		help='Specify data to send')
	
	(options, args) = parser.parse_args()
	
	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(',')
	tgtData = options.tgtData
	
	if(tgtHost == None) | (tgtPorts[0] == None):
		print('[!] You must specify at least host and port')
		print(parser.usage)
		exit(0)
	if tgtData == None:
		tgtData = 'ACK'
		
	setdefaulttimeout(1)
	initialize(tgtHost, tgtPorts, tgtData)
	

if __name__ == '__main__':
	main()

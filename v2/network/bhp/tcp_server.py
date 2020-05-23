import socket
import threading
import optparse




def launch(bind_ip, bind_port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server.bind((bind_ip, bind_port))

	server.listen(5)

	print("[*] Listening on %s:%d" % (bind_ip, bind_port))
	while True:
		client, addr = server.accept()
		print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
		client_handler = threading.Thread(target=handle_client, args=(client,))
		client_handler.start()

	

# client handling thread
def handle_client(client_socket):
    # print what client says
    request = client_socket.recv(1024)
    print("[*] Received: %s" % request)

    # send back a packet
    client_socket.send("DATA")

    client_socket.close()



def main():
	parser = optparse.OptionParser('usage: tcp_server.py '+\
		'-H <target host> -p <target port> -d <data payload>')
	parser.add_option('-H', dest='tgtHost', type='string', \
		help='Specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', \
		help='Specify target port')
	
	(options, args) = parser.parse_args()
	tgt_host = options.tgtHost
	tgt_port = options.tgtPort
	
	if (tgt_host == None) | (tgt_port == None):
		tgt_host = "0.0.0.0"
		tgt_port = 9999
	
	launch(tgt_host, tgt_port)


if __name__ == '__main__':
	main()

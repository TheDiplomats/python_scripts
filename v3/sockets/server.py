import socket

'''
# a socket is an endpoint that recieves information & data
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
print("[*] Server boot successful")

while True:
	clientsocket, addr = s.accept()
	print(f"[*] Incoming connection from {addr} received")
	# represents foreign socket object
	clientsocket.send(bytes("Succesfully connected to server", "utf-8"))
	clientsocket.close()
'''

# use headers, headers tell how long the actual message is
# prepare in advance the longest message you intend to receive
# We expect message to be less than 1,000,000,000 characters

# set header size to 10 chars
HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
print("[*] Server boot successful")
while True:
	clientsocket, addr = s.accept()
	print(f'[*] Incoming connection from {addr} received')
	
	payload = "Successfully connected to server"
	# Embdeded variable inside variable
	msg = f'{len(payload):< {HEADERSIZE}}'+ payload
	
	clientsocket.send(bytes(msg, "utf-8"))

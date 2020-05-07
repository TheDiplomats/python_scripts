import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
print("[*] Server boot successfull")

while True:
	clientsocket, addr = s.accept()
	print(f"[*]Connection received from {addr}")
	
	d = {1: "Go", 2:"Lang", 3:"Rocks!"}
	payload = pickle.dumps(d)
	
	msg = bytes(f'{len(payload):<{HEADERSIZE}}', "utf-8") + payload
	
	clientsocket.send(msg)

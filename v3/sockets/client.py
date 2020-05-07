import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

# stream of data being received set buffer size
while True:
	full_msg = ''
	new_msg = True
	while True:
		# This will receive the header and a little bit more
		msg = s.recv(16)
		if new_msg:
			print(f"New message length: {msg[:HEADERSIZE]}")
			msg_len = int(msg[:HEADERSIZE])
			new_msg = False
			
		full_msg += msg.decode("utf-8")
		if len(full_msg)-HEADERSIZE == msg_len:
			print("Full message received")
			print(full_msg[HEADERSIZE:])
			new_msg = True
			full_msg = ''

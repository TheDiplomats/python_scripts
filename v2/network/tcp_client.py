import socket

target_host = "localhost"
#target_host = "www.google.com"
target_port = 5555

# create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
client.connect((target_host, target_port))

# send data
#client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
client.send(b"echo Hello!")

# receive data
response = client.recv(4096)

print(response)
client.close()

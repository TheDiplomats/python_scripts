import socket

target_host = 'www.google.com'
target_port = 80

# New Socket Object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to client
client.connect((target_host, target_port))

# Send data
data = 'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'
client.send(data)

# Recieve data
response = client.recv(4096)

print(response)
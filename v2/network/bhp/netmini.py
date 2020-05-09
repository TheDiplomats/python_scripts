import sys
import socket
import getopt
import threading
import subprocess

# global variable definition
listen = False
command = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print("\n")
    print("Mini Network Tool\n")
    print("Usage: netmini.py -t target_host -p target_port\n")
    print("-l --listen                       - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run          - execute the given file upon receiving a connection")
    print("-c --command                      - initialize command shell")
    print("-u --upload_to_destination        - upon receiving connection upload file and write to [destination]")
    print("\n\n")
    print("Examples: \n")
    print("netmini.py -t 192.168.0.1 -p 5555 -l -c")
    print("netmini.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("netmini.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'SOMETEXT' | ./netmini.py -t 192.168.11.12 -p 135")
    print("\n")
    sys.exit(0)


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to host
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
        while True:
            # wait for data
            recv_len = 1
            response = b""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response)
            # wait for more input
            buffer = input(b"")
            buffer += b"\n"

            client.send(bytes(buffer))

    except:
        print("[*] Encountered fatal exception. Exiting")
        client.close()


def server_loop():
    global target

    # if no target is defined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # spin off thread to handle new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    # trim newline
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command, \r\n"
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    print("[*] New connection received")
    file_buffer = bytearray("", 'utf8')

  # potential bug
  #  if len(upload_destination):
  #      file_buffer = bytes("")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        else:
            file_buffer += data

    try:
        file_descriptor = open(upload_destination, "wb")
        file_descriptor.write(file_buffer)
        file_descriptor.close()
        client_socket.send(bytes("Successfully saved file to %s\r\n" % upload_destination))
    except:
        client_socket.send(bytes("Failed to save file to %s\r\n" % upload_destination))

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send(bytes("<MIN:#> "))
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(bytes(response))


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif 0 in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"

    # listen or send data from stdin
    if not listen and len(target) and port > 0:
        # read in buffer from the commandline
        # blocks so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    if listen:
        server_loop()


main()


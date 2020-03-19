import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print('Net Mini Tool')
    print('\n')
    print('Usage: net_mini.py -t target_host -p port')
    print('\n')
    print('-l   --listen                - listen on incoming port for inbound connections')
    print('\n')
    print('-e   --execute=file_to_run   - execute given file upon connection')
    print('\n')
    print('-c   --command               - initialize command shell')
    print('\n')
    print('-u   --upload=destination    - uploads file to [destination] upon connection')
    print('\n')
    print('Examples: ')
    print('\n')
    print('net_mini.py -t 192.168.0.1 -p 5555 -l -c')
    print('net_mini.py -t 192.169.0.1 -p 5555 -l -u=c:\\executable.exe')
    print('net-mini.py -t 192.168.0.1 -p 5555 -l -e=\'cat /etc/exec\'')
    print("echo 'Welcome to Net mini!' | ./net_mini.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu:',
        ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ('-h','--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e','--execute'):
            execute = a
        elif o in ('-c', '--comandshell'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False,'Unhandled Option'

    buffer = sys.stdin.read()
    client_sender(buffer)
    if listen:
        server_loop()
main()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)
        
        while True:
            recv_len = 1
            response = ''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response)

            buffer = raw_input('')
            buffer += '\n'

            client.send(buffer)
    except:
        print('[*] Net Mini encountered an exception...Exiting.')
        client.close()

def server_loop():
    global target

    if not len(target):
        target = '0.0.0.0'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler,
        args=(client_socket,))
        client_thread.start()

def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command.\r\n'
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ''
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send('Successfully saved file to %s\r\n' % upload_destination)
        except:
            client_socket.send('Failed to save file to %s\r\n' % upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)
    
    if command:
        while True:
            client_socket.send('<NM:#> ')
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(response)

import socket
import threading
import os
import signal
from sys import platform
import base64


class serverType:

    def encodefunc(self, val):
        encoded_data = base64.b64encode(bytes(val, 'utf-8'))
        print(
            f"\n\n-------- {server_name}'s Chat-Room accesskey : ( {encoded_data.decode('utf-8')} ) --------")

    def getpasskey(self, str1):
        if str1[0:7] == '192.168':
            self.encodefunc(str1[7:].zfill(8))
        else:
            self.encodefunc(str1.zfill(15))

    def broadcast(self, message, current_client):
        send_client_list = [x for x in list(
            clients_dict.keys()) if x != current_client and x != 'Server']
        for client in send_client_list:
            try:
                client.send(message)
            except:
                print('\n \t Could not send message \n')

    def rec_message(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == DISCONNECT_MESSAGE:
                    user = clients_dict[client]
                    print(f'\n \t [{user}] disconnected \n')
                    del clients_dict[client]
                    client.close()
                    self.broadcast(
                        f'\n \t [{user}] left! \n'.encode('utf-8'), client)
                    break

                else:
                    print('\t\t\t\t', message)
                    self.broadcast(message.encode('utf-8'), client)

            except:
                user = clients_dict[client]
                print(f'\n \t [{user}] disconnected \n')
                client.close()
                del clients_dict[client]
                self.broadcast(
                    f'\n \t [{user}] left! \n'.encode('utf-8'), client)
                break

    def send_message(self):
        while True:
            try:
                message = input()
                b_message = f"[{server_name}] : {message}"
                if message == DISCONNECT_MESSAGE:
                    self.broadcast('Server left'.encode('utf-8'), 'Server')
                    os._exit(0)
                self.broadcast(b_message.encode('utf-8'), 'Server')

            except:
                print('\n \t Error Occoured while Reading input \n')
                self.broadcast('Server left'.encode('utf-8'), 'Server')
                os._exit(0)

    def accept_conn(self):
        while True:

            client, address = server.accept()

            client.send('Connect'.encode('utf-8'))
            client_name = client.recv(1024).decode('utf-8')
            final_client_name = client_name
            i = 1
            while final_client_name in clients_dict.values():
                final_client_name = f"{client_name}{i}"
                i += 1

            if client_name != final_client_name:
                message = (
                    '\n \t Username updated to ['+final_client_name+']').encode('utf-8')
                client.send(message)
            clients_dict[client] = final_client_name
            print(f"\n \t [{clients_dict[client]}] joined the server \n")
            self.broadcast(f"\n \t [{clients_dict[client]}] joined! \n".encode(
                'utf-8'), client)
            client.send(f"Connected to [{server_name}]!".encode('utf-8'))

            thread = threading.Thread(target=self.rec_message, args=(client,))
            thread.start()
            print('Active threads : ' + str(threading.active_count()-1))

    def keyboardInterruptHandler(self, signal, frame):
        print('Interrupted')
        self.broadcast('Server left'.encode('utf-8'), 'Server')
        os._exit(0)


s1 = serverType()

if platform == "linux" or platform == "linux2":
    os.system('clear')
    if (os.path.exists('ip.txt')):
        os.remove('ip.txt')
    os.system("ifconfig | grep 192 | awk -F ' ' '{print $2}' > ip.txt")
    f = open('ip.txt', 'r')
    line = f.readline()
    os.remove('ip.txt')
    IP = line.strip()
elif platform == "win32":
    os.system('cls')
    IP = socket.gethostbyname(socket.gethostname())
else:
    print('Unsupported OS')
    exit(1)

print('Creating server')
server_name = input('Enter server name : ')
while not server_name.isalpha():
    print(" \n \t ERROR: The Server name should only contain a set of alphabates. \n")
    server_name = input('Enter server name : ')

clients_dict = {}
clients_dict['Server'] = server_name
PORT = 5050
DISCONNECT_MESSAGE = "exit"
s1.getpasskey(IP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

signal.signal(signal.SIGINT, s1.keyboardInterruptHandler)

thread2 = threading.Thread(target=s1.send_message)
thread2.start()
print('Created server')
s1.accept_conn()

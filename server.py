import socket
import threading
import os
import signal
from sys import platform
import base64


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

clients_dict = {}
print('Creating server')
server_name = input('Enter server name : ')
while not server_name.isalpha():
    print(" \n \t ERROR: The Server name should only contain a set of alphabates. \n")
    server_name = input('Enter server name : ')


clients_dict['Server'] = server_name

PORT = 5050


def encodefunc(val):
    encoded_data = base64.b64encode(bytes(val, 'utf-8'))
    print(
        f"\n\n-------- {server_name}'s Chat-Room accesskey : ( {encoded_data.decode('utf-8')} ) --------")


def getpasskey(str1):
    if str1[0:7] == '192.168':
        encodefunc(str1[7:].zfill(8))
    else:
        encodefunc(str1.zfill(15))


getpasskey(IP)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

DISCONNECT_MESSAGE = "exit"


def broadcast(message, current_client):
    send_client_list = [x for x in list(
        clients_dict.keys()) if x != current_client and x != 'Server']
    for client in send_client_list:
        try:
            client.send(message)
        except:
            print('\n \t Could not send message \n')


def rec_message(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == DISCONNECT_MESSAGE:
                user = clients_dict[client]
                print(f'\n \t [{user}] disconnected \n')
                del clients_dict[client]
                client.close()
                broadcast(f'\n \t [{user}] left! \n'.encode('utf-8'), client)
                break

            else:
                print('\t\t\t\t', message)
                broadcast(message.encode('utf-8'), client)

        except:
            user = clients_dict[client]
            print(f'\n \t [{user}] disconnected \n')
            client.close()
            del clients_dict[client]
            broadcast(f'\n \t [{user}] left! \n'.encode('utf-8'), client)
            break


def send_message():
    while True:
        try:
            message = input()
            b_message = f"[{server_name}] : {message}"
            if message == DISCONNECT_MESSAGE:
                broadcast('Server left'.encode('utf-8'), 'Server')
                os._exit(0)
            broadcast(b_message.encode('utf-8'), 'Server')

        except:
            print('\n \t Error Occoured while Reading input \n')
            broadcast('Server left'.encode('utf-8'), 'Server')
            os._exit(0)


def keyboardInterruptHandler(signal, frame):
    print('Interrupted')
    broadcast('Server left'.encode('utf-8'), 'Server')
    os._exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)


def accept_conn():
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
            message = ('\n \t Username updated to ['+final_client_name+']\n').encode('utf-8')
            client.send(message)
        clients_dict[client] = final_client_name
        print(f"\n \t [{clients_dict[client]}] joined the server \n")
        broadcast(f"\n \t [{clients_dict[client]}] joined! \n".encode(
            'utf-8'), client)
        client.send(f"Connected to {server_name}!".encode('utf-8'))

        thread = threading.Thread(target=rec_message, args=(client,))
        thread.start()
        print('Active threads : ' + str(threading.active_count()-1))


thread2 = threading.Thread(target=send_message)
thread2.start()
print('Created server')
accept_conn()

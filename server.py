import socket
import threading
import os
import signal

host = '127.0.0.1'
port = 55455

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients_dict = {}


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
            if message == 'exit':
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
            if message == 'exit':
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
        clients_dict[client] = client.recv(1024).decode('utf-8')
        print(f"\n \t [{clients_dict[client]}] joined the server \n")
        broadcast(f"\n \t [{clients_dict[client]}] joined! \n".encode(
            'utf-8'), client)
        client.send('Connected to server!'.encode('utf-8'))

        thread = threading.Thread(target=rec_message, args=(client,))
        thread.start()
        print('Active threads : ' + str(threading.active_count()-1))


print('Creating server')
server_name = input('Enter server name : ')
clients_dict['Server'] = server_name
thread2 = threading.Thread(target=send_message)
thread2.start()
print('Created server')
accept_conn()

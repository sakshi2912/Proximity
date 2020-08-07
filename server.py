import socket
import threading
import os
host = '127.0.0.1'
port = 55455

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients_dict = {}

def broadcast(message,current_client):
    send_client_list = [x for x in list(clients_dict.keys()) if x!= current_client and   x!='Server']
    for client in send_client_list:
        try:
            client.send(message)
        except:
            print('Could not send message')

        
def rec_message(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'exit':
                user = clients_dict[client]
                print(f'{user} disconnected ')
                client.close()
                del clients_dict[client]
                broadcast(f'{user} left!'.encode('utf-8'),client)
                break
            
            else:
                print(message)
                broadcast(message.encode('utf-8'),client)
            
        except:
            user = clients_dict[client]
            print(f'{user} disconnected ')
            client.close()
            del clients_dict[client]
            broadcast(f'{user} left!'.encode('utf-8'),client)
            break
        
def send_message():
    while True:
        try:
            message = input()
            b_message = f"[{server_name}] : {message}"    
            if message == 'exit':
                broadcast('Server left'.encode('utf-8'),'Server')
                os._exit(0)
            broadcast(b_message.encode('utf-8'),'Server')
            
        except:
            break
        
def accept_conn():
    while True:
        
        client, address = server.accept()

        client.send('Connect'.encode('utf-8'))
        clients_dict[client] = client.recv(1024).decode('utf-8')
        print(f"{clients_dict[client]} joined the server")

        broadcast(f"{clients_dict[client]} joined!".encode('utf-8'),client)
        client.send('Connected to server!'.encode('utf-8'))

        thread = threading.Thread(target=rec_message, args=(client,))
        thread.start()
        print('Active threads : '+ str(threading.active_count()-1))

print('Creating server')
server_name = input('Enter server name : ')
clients_dict['Server'] = server_name
thread2 = threading.Thread(target=send_message)
thread2.start()
print('Created server')
accept_conn()


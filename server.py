import socket
import threading
import os
host = '127.0.0.1'
port = 55455

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their uname_list
clients = []
uname_list = []

def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            print(message.decode('utf-8'))
            
            broadcast(message)
            
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            uname = uname_list[index]
            broadcast('{} left!'.format(uname).encode('utf-8'))
            uname_list.remove(uname)
            break
        
def handle2():
    while True:
        try:
            # Broadcasting Messages
            message = input()    
            if message == 'exit':
                broadcast('Server left'.encode('utf-8'))
                os._exit(0)
            broadcast(message.encode('utf-8'))
            
        except:
            break
        
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store uname
        client.send('NICK'.encode('utf-8'))
        uname = client.recv(1024).decode('utf-8')
        uname_list.append(uname)
        clients.append(client)

        # Print And Broadcast uname
        print("uname is {}".format(uname))
        broadcast("{} joined!".format(uname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        print('Active threads'+ str(threading.active_count()-1))

server_name = input('Enter server name')
thread2 = threading.Thread(target=handle2, args=())
thread2.start()
receive()

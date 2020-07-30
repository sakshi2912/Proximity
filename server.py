import socket
import threading
import os
from sys import platform

SERVER = ''

if platform == "linux" or platform == "linux2":
    SERVER = str(os.system("ifconfig | grep 192 | awk -F ' ' '{print $2}'"))
elif platform == "win32":
    SERVER = socket.gethostbyname(socket.gethostname())
else:
    print('Unsupported OS')
    os.exit(1)

PORT= 5050

def encodefunc1(val):
    print(val)
def encodefunc2(val):
    print(val)

def getpasskey(str1):
    if str1[0:9] == '192.168.':
        encodefunc1(str1[9:].zfill(7))
    else:
        encodefunc2(str1.zfill(15))


getpasskey(SERVER)
ADDR =(SERVER,PORT)
FORMAT='utf-8'
#header of 64 bytes : tells us the length of the message coming
HEADER=64
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

#handle all the communications
def handle_client(conn,addr):
    print(f"[New connection from client] {addr}")
    connected = True
    while(connected):
        #message=conn.recv(1024)
        message_length=conn.recv(HEADER).decode(FORMAT)
        if message_length:
            message_length= int(message_length)
            message= conn.recv(message_length).decode(FORMAT)
            if message==DISCONNECT_MESSAGE :
                connected=False
            print(f"[{addr}] {message}")
            conn.send('Received'.encode(FORMAT))
        
    
    conn.close()


def start_sockets():
    #handle only the incoming connections , ind clients
    server.listen()
    print(f"[LISTENING ON : {SERVER}]")
    while(1):
        #waits for a new connection 
        conn,addr=server.accept()
        thread1=threading.Thread(target=handle_client,args=(conn,addr))
        thread1.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
        

print('Starting server')
start_sockets()
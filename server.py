import socket
import threading

PORT= 5050
#fetch host IP dynamically
SERVER = socket.gethostbyname(socket.gethostname())
#one tuple to bind 
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
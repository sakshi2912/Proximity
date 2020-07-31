import socket
import threading
import os
from sys import platform
import base64
from colorama import init
import colorama
from pyfiglet import figlet_format
from termcolor import cprint
from subprocess import check_output

colorama.init()
cprint(figlet_format('PROXIMITY', font="standard"), "cyan")
print("New chat room created!!")

if platform == "linux" or platform == "linux2":
    if (os.path.exists('ip.txt')):
        os.remove('ip.txt')
    os.system("ifconfig | grep 192 | awk -F ' ' '{print $2}' > ip.txt")
    f = open('ip.txt', 'r')
    line = f.readline()
    os.remove('ip.txt')
    SERVER = line.strip()
    print(SERVER)

elif platform == "win32":
    SERVER = socket.gethostbyname(socket.gethostname())
else:
    print('Unsupported OS')
    os.exit(1)

PORT = 5050

def encodefunc(val):
    encoded_data = base64.b64encode(bytes(val, 'utf-8'))
    print(f"\n\n-------- Your Chat-Room's accesskey : ( {encoded_data.decode('utf-8')} ) --------")

def getpasskey(str1):
    if str1[0:8] == '192.168.':
        encodefunc(str1[8:].zfill(7))
    else:
        encodefunc(str1.zfill(15))


ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
# header of 64 bytes : tells us the length of the message coming
HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    try:
        print(f"[New connection from client] {addr}")
        connected = True
        while(connected):
            # message=conn.recv(1024)
            message_length = conn.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = conn.recv(message_length).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    connected = False
                print(f"\t\t\t\t\t\t\t{message}")
        print('The person has left the chat')
        conn.close()
    except ConnectionResetError:
        print('The connection is closed , you must restart the terminal')
    except ConnectionAbortedError:
        print('The connection is closed , you must restart the terminal')
    except OSError:
        print('There was some problem connecting you to the chat, please try again in some time')
        
    

def send(conn,addr):
    message_val = input()
    message = message_val.encode(FORMAT)
    message_length = len(message)
    send_len = str(message_length).encode(FORMAT)
    # padd it to header
    send_len += b' '*(HEADER-len(send_len))
    conn.send(send_len)
    conn.send(message)
   

def send_message(conn,addr):
    while(1):
        try:
            send(conn,addr)
        except:
            print('Cannot send message')
            conn.close()
    conn.close()

def start_sockets():
    server.listen()
    print(f"[LISTENING ON : {SERVER}]")
    while(1):
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        send_thread = threading.Thread(target=send_message,args=(conn,addr))
        client_thread.start()
        send_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print('Starting server')
getpasskey(SERVER)
username = input('Enter your username')
start_sockets()

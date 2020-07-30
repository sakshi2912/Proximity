import socket
import threading

PORT= 5050
SERVER = '192.168.0.105'
ADDR =(SERVER,PORT)
FORMAT='utf-8'
HEADER=64
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect to the socket
client.connect(ADDR)

def send(message_val):
    message=message_val.encode(FORMAT)
    message_length=len(message)
    send_len=str(message_length).encode(FORMAT)
    #padd it to header
    send_len+=b' '*(HEADER-len(send_len))
    client.send(send_len)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


send("Hello")
send("Peter Kavinsky")
send("Jacob Elordi")
send("aaa")
send("ooo")
#Disconnect
send("!DISCONNECT")

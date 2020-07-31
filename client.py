import socket
import threading
import base64

passkey = input("Enter your accesskey: ")
PORT = 5050
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"
# connect to the socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def decode_key(valu):
    try:
        decoded_data = base64.b64decode(valu)
        dec_ip = decoded_data.decode('utf-8')
        if len(dec_ip) == 7:
            dec_ip = '192.168.' + dec_ip.lstrip('0')
        elif len(dec_ip) == 15:
            dec_ip = dec_ip.lstrip('0')
    except:
        print(" Incorrect access key ")
        passkey = input(" Re-enter your accesskey : ")
        dec_ip = decode_key(passkey)
    
    finally:
         return dec_ip
     
SERVER = decode_key(passkey)
ADDR = (SERVER, PORT)
client.connect(ADDR)

def send(message_val):
    message = message_val.encode(FORMAT)
    message_length = len(message)
    send_len = str(message_length).encode(FORMAT)
    # padd it to header
    send_len += b' '*(HEADER-len(send_len))
    client.send(send_len)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))

send("Hello")
send("Peter Kavinsky")
send("Jacob Elordi")
send("aaa")
send("ooo")
# Disconnect
send("!DISCONNECT")

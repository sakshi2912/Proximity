import base64
import colorama
from colorama import init
from pyfiglet import figlet_format
import socket
from sys import platform
from termcolor import cprint
import threading
import os
import time
import signal

if platform == "linux" or platform == "linux2":
    os.system('clear')
elif platform == "win32":
    os.system('cls')
else:
    print('Unsupported OS')
    os._exit(1)

colorama.init()
cprint(figlet_format('PROXIMITY', font="standard"), "cyan")

passkey = input("Enter the Chat-Room's accesskey: ")
#username = input("Enter a username : ")
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
        
        if len(dec_ip) == 8:
            dec_ip = '192.168' + dec_ip.lstrip('0')
        elif len(dec_ip) == 15:
            dec_ip = dec_ip.lstrip('0')
        elif len(dec_ip)==0: 
            print("Please enter a passkey \n ")
            passkey = input(" Re-enter your accesskey : ")
            dec_ip = decode_key(passkey)
        else:
            print("Please enter the correct passkey \n ")
            passkey = input(" Re-enter your accesskey : ")
            dec_ip = decode_key(passkey)
            
    except (ConnectionRefusedError,UnicodeDecodeError,UnboundLocalError,base64.binascii.Error):
        print("Please enter the correct passkey \n ")
        passkey = input(" Re-enter your accesskey : ")
        dec_ip = decode_key(passkey)    

    finally:
        return dec_ip

SERVER = decode_key(passkey)
ADDR = (SERVER, PORT)

try:
    client.connect(ADDR)
    print(f'\n[CONNECTED TO {SERVER}]')
except ConnectionRefusedError:
        print("There is no such room available in your network \n ")
        passkey = input(" Re-enter your accesskey : ")
        dec_ip = decode_key(passkey)

#result = client.connect_ex(ADDR)

def send(u_message):
    message_val = f"[{username}] {u_message}"
    message = message_val.encode(FORMAT)
    message_length = len(message)
    send_len = str(message_length).encode(FORMAT)
    # padd it to header
    send_len += b' '*(HEADER-len(send_len))
    client.send(send_len)
    client.send(message)

def send_message():
    while(1):
        try:
            send(input())
        except:
            print('Cannot send message')
            client.close()
    client.close()
        
def rec_msg():
    try:
        connected = True
        while(connected):
            # message=conn.recv(1024)
            message_length = client.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = client.recv(message_length).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    connected = False
                print(f"\t\t\t\t\t\t{message}")
        print('The person has left the chat')
    except (ConnectionResetError,ConnectionAbortedError):
        print('The connection is closed , you must restart the terminal')
    except (OSError,ConnectionRefusedError):
        print('There was some problem connecting you to the chat, please try again in some time')
    client.close()
    
username=input("\nEnter your username : ")
send_thread = threading.Thread(target=send_message)
rec_thread = threading.Thread(target=rec_msg)
send_thread.start()
rec_thread.start()

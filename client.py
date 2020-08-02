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
import sys

if platform == "linux" or platform == "linux2":
    os.system('clear')
elif platform == "win32":
    os.system('cls')
else:
    print('Unsupported OS')
    exit(1)

colorama.init()
cprint(figlet_format('PROXIMITY', font="standard"), "cyan")

passkey = input("Enter the Chat-Room's accesskey: ")
#username = input("Enter a username : ")
PORT = 5050
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def decode_key(valu):
    try:
        decoded_data = base64.b64decode(valu)
        dec_ip = decoded_data.decode('utf-8')

        if len(dec_ip) == 8:
            dec_ip = '192.168' + dec_ip.lstrip('0')
        elif len(dec_ip) == 15:
            dec_ip = dec_ip.lstrip('0')
        elif len(dec_ip) == 0:
            print("Please enter a passkey \n ")
            passkey = input(" Re-enter your accesskey : ")
            dec_ip = decode_key(passkey)
        else:
            print("Please enter the correct passkey \n ")
            passkey = input(" Re-enter your accesskey : ")
            dec_ip = decode_key(passkey)

    except (ConnectionRefusedError, UnicodeDecodeError, UnboundLocalError, base64.binascii.Error):
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


def send(u_message):
    message_val = u_message
    message = message_val.encode(FORMAT)
    message_length = len(message)
    send_len = str(message_length).encode(FORMAT)
    # padd it to header
    send_len += b' '*(HEADER-len(send_len))
    client.send(send_len)
    client.send(message)
    if u_message == DISCONNECT_MESSAGE :
        print('You have disconnected')
        client.close()
        os._exit(0)


def send_message():
    client.send(username.encode(FORMAT))
    while(client.fileno()):
        try:
            send(input())
        except:
            print('Cannot send message')
            client.close()
            break
    sys.exit()


def rec_msg():
    try:
        uname=client.recv(10).decode(FORMAT)
        while(True):
            message_length = client.recv(HEADER).decode(FORMAT)
            if message_length:
                try:
                    message_length = int(message_length)
                except:
                    exit(0)

                message = client.recv(message_length).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    client.close()
                    break
                print(f"\t\t\t\t\t\t{uname} > {message}")
        print(f'{uname} left the chat')
        
    except (ConnectionResetError, ConnectionAbortedError):
        print('The connection is closed , you must restart the terminal')
        sys.exit(0)
    except (OSError, ConnectionRefusedError):
        print('There was some problem connecting you to the chat, please try again in some time')

    
    



username = input("\nEnter your username : ")
send_thread = threading.Thread(target=send_message)
rec_thread = threading.Thread(target=rec_msg)
send_thread.start()
rec_thread.start()

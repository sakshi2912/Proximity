import socket
import threading
import os
import signal
from sys import platform
import sys
import base64


if platform == "linux" or platform == "linux2":
    os.system('clear')
elif platform == "win32":
    os.system('cls')
else:
    print('Unsupported OS')
    exit(1)

passkey = sys.argv[1]
PORT = 5050
DISCONNECT_MESSAGE = "exit"


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


IP = decode_key(passkey)

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))


def receive():
    while True:
        try:

            message = client.recv(1024).decode('utf-8')
            if message == 'Connect':
                client.send(username.encode('utf-8'))

            elif message == 'Server left':
                print('\nServer has disconnected\n')
                os._exit(0)

            elif message[-5:] == 'left!':
                print('\n \t', message, '\n')

            elif message == 'Connected to server!':
                print('\n \t Connected to the Server! \n')

            else:
                print('\t\t\t\t', message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        try:
            input_val = input()
            if input_val == DISCONNECT_MESSAGE:
                client.send(DISCONNECT_MESSAGE.encode('utf-8'))
                client.close()
                print('You will be disconnected')
                os._exit(0)
            else:
                message = f'[{username}] : {input_val}'
                client.send(message.encode('utf-8'))
        except:
            print('\n \t Error Occoured while Reading input \n')
            client.send(DISCONNECT_MESSAGE.encode('utf-8'))
            client.close()
            print('You will be disconnected')
            os._exit(0)


def keyboardInterruptHandler(signal, frame):
    print('Interrupted')
    client.send(DISCONNECT_MESSAGE.encode('utf-8'))
    client.close()
    print('You will be disconnected')
    os._exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

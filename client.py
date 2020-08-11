import socket
import threading
import os
import signal
from sys import platform
import sys
import base64


class clientType:

    def decode_key(self, valu):
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
                dec_ip = self.decode_key(passkey)
            else:
                print("Please enter the correct passkey \n ")
                passkey = input(" Re-enter your accesskey : ")
                dec_ip = self.decode_key(passkey)

        except (ConnectionRefusedError, UnicodeDecodeError, UnboundLocalError, base64.binascii.Error):
            print("Please enter the correct passkey \n ")
            passkey = input(" Re-enter your accesskey : ")
            dec_ip = self.decode_key(passkey)

        finally:
            return dec_ip

    def receive(self):
        global username
        while True:
            try:

                message = client.recv(1024).decode('utf-8')
                if message == 'Connect':
                    client.send(username.encode('utf-8'))

                elif message == 'Server left':
                    print('\nServer has disconnected\n')
                    os._exit(0)

                elif 'Connected to' in message:
                    print('\n \t ', message, '\n')

                elif 'Username updated to [' in message:
                    print(message)
                    username = message[25:-1]

                else:
                    print('\t\t\t\t', message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
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

    def keyboardInterruptHandler(self, signal, frame):
        print('Interrupted')
        client.send(DISCONNECT_MESSAGE.encode('utf-8'))
        client.close()
        print('You will be disconnected')
        os._exit(0)


c1 = clientType()

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
IP = c1.decode_key(passkey)

username = input("Enter your username: ")
while not username.isalpha():
    print(" \n \t ERROR: The username should only contain alphabates. \n")
    username = input('Enter server name : ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))


signal.signal(signal.SIGINT, c1.keyboardInterruptHandler)

receive_thread = threading.Thread(target=c1.receive)
receive_thread.start()

write_thread = threading.Thread(target=c1.write)
write_thread.start()
